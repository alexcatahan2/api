from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix = "/workouts",
  tags= ['Workouts']
)

@router.get('/')
def get_user_workouts(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  workouts = db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()

  return workouts

#@router.post('/')
#def create_workout(workout : make schema db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):