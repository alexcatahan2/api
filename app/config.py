from pydantic import BaseSettings

#here we can basically provide a list of all of the environment varaibles we need set
class Settings(BaseSettings):
  database_hostname:str
  database_port:str
  database_password:str
  database_name:str
  database_username:str
  secret_key: str
  algorithm:str
  access_token_expire_minutes:int
  
  class Config:
      env_file = ".env"

settings = Settings() #create an instance of the settings class that defines the env vars and its going to perform all of the validations

"""
  this makes using env vars so much easier because it will type validate ( and since env vars are
  read in as strings it will do the proper conversion, so long as the string can be converted i.e. '60' to 60)
  and since there will be lots of env vars big applications need and it can be hard to keep track if we're missing
  one, making this pydentic model will raise an error if one is missing and tell us what is missing9
"""