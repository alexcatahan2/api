from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from .config import settings


#when you use sql alchemy you talk to the databse with that, so you dont really need this logic down here with the postgres driver
#psycog lets us set up a connection to our database
# while True:
# # Connect to an existing database
#   try:
#     conn = psycopg2.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', password = 'a6$7W1N!xx', cursor_factory= RealDictCursor)
#     cursor = conn.cursor()
#     print("databse connection was successful")
#     break
#   except Exception as error:
#     print("Connecting to database failed")
#     print(error)
  # with psycopg.connect(host = 'localhost', dbname = 'fastapi', user = 'postgres', 
  #                     password = 'a6$7W1N!xx') as conn:
  #     # Open a cursor to perform database operations
  #     with conn.cursor() as cur:
  #       print('Succesfully connected to database!!')

  #       posts = cur.execute("SELECT * FROM posts")
  #       print(posts)
  #       break
#you have to specificy connection string, where is our postgres database located?
#format of the connection string: postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
#postgres is a sql based database

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

#the engine is what is responsible for sql Alc to connect to a postgres database:

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#when you actually want to talk to the sql database you have to make use of a session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

#we have to define our base class
#all of the models that we define to actually create our tables in postgress will be extended this base class

Base = declarative_base()

#Dependency (dont know what this is yet):
#this is how we get a session and we can send sql statements to it and finnaly once its done we can close it out
#we can keep calling this function aytime we get a request to any of our api endpoints
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

