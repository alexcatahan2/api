from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
  tags = ["Authentication"]
)

#this is goig to be a post request because the user is going to provide credentials 
#generally when you want to send data in one direction its going to be a post request

@router.post("/login", response_model = schemas.Token)
def login_user(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
  login_attempt = db.query(models.User).filter(models.User.email == user_credentials.username).first()
  if login_attempt == None:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
  if not utils.verify(user_credentials.password, login_attempt.password):
     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
  
  #create a token, then return the token

  access_token = oauth2.create_acces_token(data = {"user_id": login_attempt.id})
  return {"access_token": access_token, "token_type" : "bearer"}
  
  