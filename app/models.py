#every model represnts a table in our databse
from sqlalchemy import TIME, TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text, DATE
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
  __tablename__ = "posts" 
  id = Column(Integer, primary_key = True, nullable = False)
  title = Column(String, nullable = False)
  content = Column(String, nullable = False)
  published = Column(Boolean, server_default = 'TRUE', nullable = False)
  created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
  owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)

  owner = relationship("User")
  #made an object "object" show up in the return by passing in a pydantic model of the user return
  #the pydentic model of the user return gets its information from the User table, the entry that 
  #matches the autorized id of course

  #set up a relationship that tells sql alchemy to automatically fetch some piece of information
  #base off of the relationship
class User(Base):
  __tablename__ = "users"
  email = Column(String, nullable = False, unique = True)
  password = Column(String, nullable = False)
  id = Column(Integer, primary_key = True, nullable = False)
  created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = ('now()'))
  firstName = Column(String, nullable = False, server_default = "first name")
  lastName = Column(String, nullable = False, server_default = "last name")

class Vote(Base):
  __tablename__ = "votes"
  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key = True)
  liked_post = relationship("Post")
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key = True)
  user_liked = relationship("User")

class Workout(Base):
  __tablename__ = "workouts"
  id = Column(Integer, primary_key = True, nullable = False)
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
  start = Column(TIMESTAMP(timezone=True), nullable = False, server_default = ("now()"))
  stop = Column(TIMESTAMP(timezone=True), nullable = False, server_default = ("now()"))
  length = Column(Integer, nullable = False, server_default = "0")
  date = Column(DATE, nullable = False, server_default = ("CURRENT_DATE"))

class Exercise(Base):
  __tablename__ = "exercises"
  exercise_id = Column(Integer, nullable = False, primary_key = True)
  workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable = False)
  type = Column(String, nullable = False, server_default = "exercise")
  repititions = Column(Integer, nullable = False, server_default = "10")
  weight = Column(Integer, nullable = False)
  start = Column(TIMESTAMP(timezone=True), nullable = False, server_default = ("now()"))
  stop = Column(TIMESTAMP(timezone=True), nullable = False, server_default = ("now()"))