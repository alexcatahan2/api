from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix = "/exercises",
  tags= ['Exercises']
)

