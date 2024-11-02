import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_USER = os.getenv("DATABASE_USER")  
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD") 
    DATABASE_DB = os.getenv("DATABASE_DB")
    DATABASE_HOST = os.getenv("DATABASE_HOST") 
    DATABASE_PORT = os.getenv("DATABASE_PORT") 

    DATABASE_URL = os.getenv("DATABASE_URL")  

    SECRET_KEY = os.getenv("SECRET_KEY")

    FLASK_ENV = os.getenv("FLASK_ENV")

settings = Settings()
