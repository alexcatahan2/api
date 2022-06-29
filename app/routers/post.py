from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
  prefix = "/posts", #this simplifes our path route now the /post in all the routes arent needed
  tags = ['Posts'] #adds a sort of group name so in the documentation these related routes are grouped together
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db : Session = Depends(get_db), limit : int = 10, skip : int = 0, search:Optional[str] = ''):
  #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  #raw SQL query action:
  # cursor.execute("SELECT * FROM posts")
  # posts = cursor.fetchall()
  posts = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  
  return posts



@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post) #by passing the db and createing the sessions as a param it makes it a dependecy which makes tesitng easier, it gives us access to our database object
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #we extract data from the front end which is the post parameter #the current_user depedendcy requires uses to be logged in to create a post
   #get_current_user is a dependcy for this, create_post, function which means whenever the create_post function
   #is called when this endpoint is hit, the first thing that will happen is get_current_user will be called
   #and get_current_user will verify the users access with the provided access token, now we can access the user_id because it is supplied by get_current_user
  
   #the stars unpack the dictionary to get it into a format to pass into the Post method
  created_post = models.Post(owner_id=current_user.id, **post.dict())  #creates a brand new post by unpacking the dict
  db.add(created_post) #add the post to our database
  db.commit() #commit it so it actually shows up in our databse
  db.refresh(created_post) #essentially retrieves the new post we just created and store it in created_post
  # print(post)
  # print(post.dict()) #when data was extracted it was saved as a pydantic model, which have a built in .dict() function that converts it into a dictionary
  # cursor.execute("INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *",
  #                 (post.title, post.content, post.published))
  # created_post = cursor.fetchone()
  # conn.commit()
  print(current_user.email)
  return created_post


@router.get("/{id}", response_model= schemas.PostOut) #the id field represents a path parameter
def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #id: int lets fastAPI automatically validate right data type and also changes the path paramter to an int
  post = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(models.Vote, models.Post.id==models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  
  #filter(models.Post.id == id).first()
  #raw SQL action:
  # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
  # post = cursor.fetchone()

  if post:
     return post
  else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id:{id} was not found")
  
  
  
  # post = find_post(id)
  # if not post:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
  #    #imoprt HTTPExceptions, this is a clean way to raise a imformative error for the user
  # return {"post-detail": f"here is your post: {post}"}
#schema (defined using pydantic):
# title:str, content:str 


  # payLoad: dict = Body(...) 
  # this is going to extract all of the fields
  # from the body of the request and basically
  # convert it into a python dictionary and 
  # store it inside a variable named payLoad

  #new_post: Post
  #references the pydantic model of what a post
  #should look like a stores it inside a variable 
  #called new_post and fastAPI is automatically
  #going to validate if the posted data matches the model
  #also automatically accesses the data


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #db param is the database dependency
  post = db.query(models.Post).filter(models.Post.id == id)

  
  #raw SQL:
  # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
  # deleted_post = cursor.fetchone()
  # conn.commit()
  if post.first() == None:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
  if post.first().owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"post with id: {id} does not belong to you")
  post.delete(synchronize_session=False) #this will delete the post found with the query
  db.commit() #this will commit the changes to the database so the post is acutlaly deleted
  return Response(status_code=status.HTTP_204_NO_CONTENT)

#   removed = remove_post(id)
#   if removed:
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#   else:
#     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
  


@router.put("/{id}", response_model = schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #we extract data from the front end which is the post parameter
  post_query = db.query(models.Post).filter(models.Post.id == id)
  
  post_to_update = post_query.first()
  # cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *", (post.title, post.content, id))
  # updated_post = cursor.fetchone()
  # conn.commit()
  if post_to_update == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
  if post_to_update.owner_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = f"post with id: {id} does not belong to you")
  post_query.update(post.dict(), synchronize_session=False)
  db.commit()
  return post_query.first()
 
 
