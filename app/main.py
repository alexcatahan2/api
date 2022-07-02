from fastapi import FastAPI
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#neeed these two to import the models and dependcany
from . import models #.means currenbt directory
from .database import engine

#import the routers to get access to our path routes
#we put our path routes into different locations so our main isn't as big
from .routers import post, user, auth, vote #import the post.py and users.py from our routers folder
app = FastAPI()

#middleware is basically a function that runs before every request
"""
if someone sends a request before our app, before it actually fgoes through all these routers
itll go through the middleware which will perform an operation
"""
origins =["*"]
app.add_middleware(
  CORSMiddleware,
  allow_origins="*", #specify the origins we want to allow/ what domains do we want to be able to talk to our api
  allow_credentials=True, 
  allow_methods=["*"], #we can allow only specific http methods, for example if we only wanted clients to retrieve data from our api we could only allow get requests
  allow_headers=["*"] #we can allow specific headers
)
#use almebic as a database migration tool and dataabde managemnet tool

#pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto") #telling passlib what hashing algoritm we want to use


#uses passlib to handle password hashing, which works with different algorithms
#one of the popular ones, and the one that this app uses is bcrypt algorithm

#recap: 6-25 8:46 about 5 hours into 
# """
#   using fastapi, postgres as our database, psycog to comminucate
#   with our databse in python, sqlalchmey to abstract all the raw
#   SQL away
# """


#this line of code creates all of our models that we made in other files

# models.Base.metadata.create_all(bind = engine) #this creates the tables we defined into postgres
"""
now that we have alembic, we no longer need this command, this is the commend that told sqlalchemny to run
the create statement so it generated all of the tables when it first started up, but since we use alembic
we nolonger need it, but it wont break anything

"""

#to work with a postgres databse within a python application we need a postgres driver which is what psycog is
#uses psycopg for the SQL database driver, even an ORM needs it because they can speak to a database
#uses unicrov to host server 
#uses pydantic library to define what our schema should look like, this is its own complete seperate library from fstapi

#to change the defualt status code of a path you can include status_code
#as a parameter to that function, to change it when an error occurs
#you can you raise an HTTPException and set it to the desired 
#status code
#Use sqlAlchemy ORM to abstract away SQL


app.include_router(post.router) #import the router object from post.py 
# """
# When we get an http request we go down the list like we normally do, 
# because fastapi reads from top to bottom and app.includerouter is the first app object that we refere3ce
# and it includes our post.router, and then the request will go to the included router, in this case
# its in post.py, and it will look at all of the routes, this is how we split our code
# into speereate files
# """
#uses pyton-jose with cryptography backedn to create JWT toekn


app.include_router(user.router) #grabs the router object from the user file which essentially imports all of the routes in the file

app.include_router(auth.router)

app.include_router(vote.router)
#This is called a path oepration or route:made up of two components
@app.get("/")     #declarator? magic that turns it into a path operation so someone can hit this endpoint
async def root():     #function 
    return {"message": "welcome to my API!!!!"}


# function is a plain old function
# asycn is need only if youre performing an
# asynchronous task. It's just a regular function 
# named root that is defined

#@app.get("/")
#@ is just declarator syntax
#app is a refernece to our fastAPI instance
#get is the http method that the function will use
#/ is the route path, basically the path after the speciic domain name of our API


    
  
  # index = find_index(id) #found the index of post to update
  # if index == None: #if the post doesnt exists the index will by None so handle that 
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
  # #if index does exist we want to convert the extracted post to a dict, give it the extraxted id, and then update the proper element in database dict
  # post_dict = post.dict()
  # post_dict['id'] = id
  # my_posts[index] = post_dict
  # return {"data": post_dict}
