from time import time
import fastapi
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #token url is basically the login endpoint
#We need to provide the secret key, the algorithm we want to use, HS256, and we need to provide the expiration time of the token
#if we give a plain token without an expiration date that means that user is logged in forever

#needed:
  #SECRET_KEY
  #Algorithm
  #Expiration time: dicate how long the uer should be looged in after they perform a login 

SECRET_KEY = settings.secret_key#some arbitrary long text
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acces_token(data: dict):
  to_encode = data.copy()  #make a copy of passed in data so we dont maniuplate the acutal data
  expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES) #create the expire token by grabbing the current time and adding on 30 minutes using time delta #important to use utcnow vs just now
  to_encode.update({"exp": expire}) #this adds the expiration time onto the data

  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM) #this method actually creates the jwt token
  #the first prop is everything we want to put into the payload, the second is the secret key, the third is the algorithm
  return encoded_jwt

def verify_access_token(token:str, credentials_exception):
  try:  #this decode function will raise an exception if the signature is wrong
    payload = jwt.decode(token, SECRET_KEY, ALGORITHM) #this is decoding the token that was supplied by client to then vdrify it
    #this puts all of the payload data from the token into the variable payload^
    
    extracted_id:str = payload.get("user_id") #gets the specific data that we want from the token, in this case our desired data is called users_id

    if id is None: #if there is no id in the payload that was passed back by the client
      raise credentials_exception #the credentials dont match up
    token_data = schemas.TokenData(id = extracted_id)
  except JWTError:
    raise credentials_exception
  return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f'could not validate credentials',
  headers={"WWW_Authenticate": "Bearer"})
  
  #the token is not directly connected to a user, the user id that made the token is just embedded in the token
  #therefore to get the user from the token we have to extract the id and then query our databse again
  #to get the user the is associated with the token:

  token = verify_access_token(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == token.id).first()

  return user