from curses.ascii import HT
from email.policy import HTTP
from requests import post
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/vote",
  tags = ['Votes']
)

@router.post("/")
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  if not db.query(models.Vote).filter(models.Post.id == vote.post_id).first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "the post you want to like was not found")
  vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
  found_vote = vote_query.first()
  if(vote.dir == 1):
    if found_vote:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="you already liked this post")
    new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return {"like succesful" : new_vote}
  else: 
    if not found_vote:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you have not liked this post")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "took your like away"}


#get the likes of a specified post
@router.get('/{id}')
def get_likes(id:int, db:Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
  likes = db.query(models.Vote).filter(models.Vote.post_id == id).all()
  return likes

