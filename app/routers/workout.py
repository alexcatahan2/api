from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix = "/workouts",
  tags= ['Workouts']
)

@router.get('/', response_model=List[schemas.Workout])
def get_user_workouts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  workouts = db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()

  return workouts

@router.post('/', response_model=schemas.Workout)
def create_workout(workout: schemas.WorkoutCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  created_workout = models.Workout(user_id = current_user.id, **workout.dict())
  db.add(created_workout)
  db.commit()
  db.refresh(created_workout)
  return created_workout

"""
when you start the workout timer on the front end a workout will be created, but the stop time and length 
will need to be updated, so when you hit the stop the workout button in the front end the update path route
will take care of make the updates to the stop time and length of the workout

HOW DO YOU GET THE EXERCISES TO HAVE THE SAME WORKOUT_ID AS THE RIGHT WORKOUT?

When you create a workout the path route will return the workout you created and you can save the
id of the workout to feed the exercises that you complete during each workout
"""

@router.put('/{id}', response_model=schemas.Workout)
def update_workout(id : int, workout: schemas.WorkoutCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  workout_query = db.query(models.Workout).filter(models.Workout.id == id)
  workout_to_update = workout_query.first()

  if workout_to_update == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"workout with id : {id} was not found")
  if workout_to_update.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"workout with id : {id} does not belong to you")
  
  workout_query.update(workout.dict(), synchronize_session=False)
  db.commit()

  return workout_query.first()