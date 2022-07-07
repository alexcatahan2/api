#put schemas here just so we dont clutter up our main.py file
from datetime import datetime, time, date
from optparse import Option
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr, conint
from typing import Optional

from sqlalchemy import Date, Time
# #define post schema
# class Post(BaseModel):
#   title:str
#   content:str
#   published: bool = True #optional field because has a default value
#   #rating: Optional[int] = None #this is a fully optionaly field using Optional from typing, and by default it is None or nothing
class UserCreate(BaseModel):
  email:EmailStr
  password:str
  firstName:str
  lastName:str


class UserReturn(BaseModel):
  id:int
  email: EmailStr
  created_at: datetime
  firstName:str
  lastName:str

  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email:EmailStr
  password:str

class PostBase(BaseModel):
  title:str
  content:str
  published: bool = True


class PostCreate(PostBase): #extends PostBase
  pass #pass just means it just and nothing else accepts everything it iherits from PostBase

class Post(PostBase):
  id:int
  created_at:datetime
  owner_id:int
  owner: UserReturn

  class Config:
    orm_mode = True #we added this so the extracted orm model can be converted to match this pydantic model

class PostOut(BaseModel):
  Post: Post
  likes: int

  class Config:
    orm_mode = True


class Token(BaseModel):
  access_token: str
  token_type:str
  user: UserReturn

class TokenData(BaseModel):
  id: Optional[str]

class Vote(BaseModel):
  post_id:int
  dir: conint(le=1)

class VoteReturn(Vote):
  pass
  liked_post: Post
  user_liked: UserReturn

  class Config:
    orm_mode = True #we incldue this because the liked_post we want to format and return is recieved as a orm_model

class Workout(BaseModel):
  user_id: int
  start: time
  stop:time
  length:time 
  id:int
  date: date

  class Config:
    orm_mode = True

class WorkoutCreate(BaseModel):
  start: time
  stop: time
  length: time

  class Config:
    orm_mode = True

class Exercise(BaseModel):
  exercise_id: int
  workout_id : int
  user_id : int
  type : str
  repititions: int
  weight: int
  start : time
  stop: time

class ExerciseCreate(BaseModel):
  workout_id : int
  type : str
  repititions: int
  weight: int
  start : time
  stop: time