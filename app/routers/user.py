from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix = "/users",
  tags= ['Users']
)

@router.get("/", response_model= List[schemas.UserReturn])
def getUsers(db : Session = Depends(get_db)):
  users = db.query(models.User).all()
  return users

@router.get("/{id}", response_model= schemas.UserReturn)
def get_user(id: int, db : Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()
  print(user)
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"there is no user with id: {id}")
  return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserReturn)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  #create hash of password- user.password
  #reference the password conext where we defined bcrypt as out hashing algorithm
  user.password = utils.hash(user.password) #this updates the pydantic model of the user, gotten from the body (in postgres for now) to be the hashed password
  created_user = models.User(**user.dict())
  db.add(created_user)
  db.commit()
  db.refresh(created_user)
  return created_user


@router.delete("/{id}", response_model= schemas.UserReturn)
def delete_user(id:int, db : Session = Depends(get_db)):
  user_query = db.query(models.User).filter(models.User.id == id)
  delete_user = user_query.first()
  if delete_user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id:{id} was not found")
  user_query.delete()
  db.commit()
  return delete_user

@router.put("/{id}", response_model= schemas.UserReturn)
def update_user(id:int, update_user: schemas.UserCreate, db: Session = Depends(get_db)):
  user_query = db.query(models.User).filter(models.User.id == id)
  user = user_query.first()
  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"user with id:{id} was not fonud") 
  user_query.update(update_user.dict(), synchronize_session=False)
  db.commit()
  return user_query.first()