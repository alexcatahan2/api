from sqlalchemy import func
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix = "/exercises",
  tags= ['Exercises']
)

@router.get('/', response_model=schemas.Exercise)
def get_user_exercises(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  exercises = db.query(models.Exercise).filter(models.Exercise.user_id == current_user.id).all()
  return exercises

@router.get('/{workoutID}')
def get_workouts_exercises(workoutID : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  exerices = db.query(models.Exercise).filter(models.Exercise.workout_id == workoutID).all()

  return exerices

@router.get('/sets/{workoutID}')
def get_exercise_sets(workoutID: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  sets = db.query(models.Exercise.type, func.count(models.Exercise.type).label('sets')).group_by(models.Exercise.type).all()
  return sets


@router.post('/')
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  created_exercise = models.Exercise(user_id = current_user.id, **exercise.dict())
  db.add(created_exercise)
  db.commit()
  db.refresh(created_exercise)
  return created_exercise

@router.put('/{id}')
def update_exercise(id: int, exercise: schemas.ExerciseCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  exercise_query = db.query(models.Exercise).filter(models.Exercise.user_id == id)
  exercise_to_update = exercise_query.first()

  if exercise_to_update == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'exercise with id : {id} was not found')
  if exercise_to_update.user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "exercise with id: {id} does not belong to you")
  
  exercise_query.update(exercise.dict(), synchronize_session=False)
  db.commit()
  return exercise_query.first()