#any time you create a new folder make sure you create a dummy
#file with this new name which will ensure it is a 
#python package., you dont even have to put anything in it




# """
# notes about databases:
#    a data base is a collection of organized data that can easily
#    be accessed or manages, data is like registered users or posts that are created

#    We never actaully work with databases directly, instead there is a middle man which
#    is called a database management system (DBMS) when we want to work with a database
#    we will send a request to the DBMS and then that will actually perform the operation
#    and will send the result back to us

#    two types of main databases: Relational and NoSQL
#    relational databases are usually sequel styles databases
#    In the course We are going to work with relational databases and
#    specifically POSTGRESQL, but all of the databases are almost the same because
#    they all at the end of the day use SQL with slightly different implementation

#    SQL or Structured Query Language - language used to communicate with DBMS
#    when we want to perform an operation on a database we will send a specific 
#    SQL statement to the DBMS its then going to take that statement and perform the
#    operation on the database and itll then send the result back to us
#    
#     databases have data types just like any programming langauge
# """

# """
# notes about tables:

#   very imoprtant when working with relatinoal databses
#   a table represents a subject or event in an application
#   you will have a table for each part of your application for exmpale:
#   if ecommerce youll ahve a table for users and products and purches

#   all of the tables will form some sort of relationship

#   a table is made up of columns and rows
#     each colkumn represents a different attribute
#     each row represents a different entry in the table 
#     for example:
#         ID           name           Age          Sex
#         192034       Alex          19             M
#         38903         JAne         20             F
#         382904        Jet           20            M
#         32834         Anthony       20            M

#   since databases have datatypes when you create a column within a table you need 
#   to specify what type of datatype you want to use
#   Numeric:   Int, decimal, precision...
#   Text:      Varchar, text
#   bool:      boolean
#   sequence:    arrary

#   when we create a table we need to specify a primary key; a table can have one and only one promary key
#   a primary key is a column or group of columns that uniquely identifies each row in a table
#   in the user table example the primary key is the ID column, in the primary key column each entry MUST
#   BE UNIQUE 
#   it is up to you to decide which column uniquely defines each record, does not have to be an id colummn,
#   for example an email column commonly works, also phone numbers because generally you cant sign 
#   up with two emails or phone numbers for different account

#   A UNIQUE constraint can be applied to any column to make sure every record has a unique value for that column


#   NULL contraint
#   By default, when adding a new entry to a datebase, any column
#   can be left blank. When a column is left blank, it has a null value
#   If you need column to be properly filled in to create a new record, a NOT NULL 
#   contraint can be added to the column to ensure that the column is never left blank,
#   for example a user should HAVE to make a username and password, so those columns should be
#   constrained to NOT NULL
# """


# """
#   Key words in SQL:
#   SELECT - basically get, can specify specific column names to get or just all by *
#   FROM - specifies table to select from
#   WHERE - can specify qualities of entries you want to reutrn i.e. WHERE price > 20 or WHERE name = 'TV%'
#   ORDER BY - specifies order you want the data to come back in i.e. ascending or descending
#   LIMIT - limits the amount of entries returned, can be chanined with OFFSET which will skip certain amount of entries that match the filters 

#   SQL command for entering a brand new entry into our data base:
  
#   INSERT INTO tableName(listOfColsWeWantToPassDataInto) VALUES(values for each column)
#   actual example:
#   INSERT INTO product(name, price, inventory) VALUES('TV', 800, 100)

#   SQL Command for deleting an entry from a database:

#   DELETE FROM tableName WHERE id = product you want to delete

#   SQL command for updating a row:

#   UPDATE tableName SET col = 'updated info', col = 'updated info' WHERE id = enterID
# """

# """
#   Object Relational Mapper (ORM):
#     way to communicate with a database
#     Layer of abstraction that sets between the database and us, our fastapi application
#     The fastAPI sever never talks to the database, we instead talk to the orm and the orm will talk to the database
#     We can perofrm all database operations through traditional python code. NO MORE SQL!

#     fastAPI can use regular python code to talk to on ORM, which will then convert it into SQL and then
#     talk to the database, by doing it like this we can abstract away the SQL and use normal python

#     Insead of manually defining tables in portgres, we can 
#     degine our tables as python models ex:

#     class Post(Base):
#       __tableName__ = "posts"

#       id = Column(Intgeer, primary_key = true, index = true)
#       title = Column(String, index = True, nullable = False)
#       content = Column(String, nullable = False)
#       published = Column(Boolean)

#     Queries can be made exclusively through python code. NO SQL is necessary ex:
#     db.query(models.Post).filter(models.Pos.id = id).first()

#     SQLALCHEMY is one of the most popular python ORMS
#     This is a standalone libaray and has no association with FastAPi. it can be used with any other pyhon 
#     web frameworks or any python based opplication
# """

# """
#  difference between ORM model and pydantic model:
#   schema/pydantic model: define the straucture of a request and response
#                         this ensures that when a user wants to create a post, the 
#                         request will only go throguh if it has fields matching the model, 
#                         acts as a type of validation/ type validation, works with requests AND response
#   SQL alchemy model (defined table): Responsilbe for defining the columns of our "posts" (table)
#                                       withing postgres
#                                       # is used to query, create, delete, and update entries within the 
  
# """

"""
  JWT Token Authentication:
    when youre working with authenticaiton  theres really two main ways to tackle authenticaiton:
      session based authentication: we store somethingon our backend server or our apir in this case to track
         whether a user is logged in
      OR
      JWT Token based authentication: the idea behind this is that its stateless, which means theres nothing
      in our backend, api, databse that actually keeps track or stores some sort of information about wheter
      a user is logged in or logged out, the Token itself (which we do not store in our api, its actually stored in 
      the front end in our clients) keeps track of whether a user is logged in or not

"""

"""
  To connect/associate tables in our data base we can set up a relationship between our tables
  We do this by adding a new column in one of our tables called a Foreign Key, and the foreign key is how we tell 
  sequeul that this column is connected to a different table, and in the foreign key we specify two things,
  we specify the table that it should be connected to, and we specify what specific column in the table should 
  it be

"""

"""
  IN PRODUCTION you wouldnt ues a .env file to set all of your env vars, 
  youd have it on your machine, but in devolopment its totlaly fine
"""

"""
  join the posts and users tables on the owner id and user id column, group the entries by their created user
  and then count the amount of entries created by each user

  SELECT users.id, email, COUNT(owner_id) AS users_post_count FROM posts RIGHT JOIN users ON posts.owner_id = users.id group by users.id;
"""

"""
Databse migrations
  developers can track changes to code and rollback code easily with GIT. Why cna't we do the same for databse models/tables
  databse migrations allow us to incremnetially track changes to database
  schema and rollback changes to any point in time 
  we will use a tool called alembic to make changes to our databse
  Alembic can also automatically pull databse models from SQLAlchemy and generate the proper tables
"""