import json,os
from archive.contextmanager import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#postgres url
URL_DATABASE = 'postgresql://postgres:password@localhost:5432/movie_db'

#creating engine 
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)
    



class Database:

    #creating database if file doesnot exist
    @staticmethod
    def create_database(DATABASE):
    #creating the folder if it doesn't exist
        os.makedirs(DATABASE["DB_FOLDER"], exist_ok=True)
        for key, filename in DATABASE["DB_FILES"].items():
            filepath = os.path.join(DATABASE["DB_FOLDER"],filename)
            try:
                with open(filepath,"x") as file:
                    json.dump({},file) # starting with an empty dictionary
                print(f"Created database: {filepath}")

            except FileExistsError :
                print(f"file already existed {filepath}")

    @staticmethod
    #load json files
    def read_json(DATABASE,db_type):
        filepath = os.path.join(DATABASE["DB_FOLDER"],DATABASE["DB_FILES"][db_type])
        try:
            with ContextManager(filepath,"r") as file:
                data = json.load(file)
                return data
        except FileNotFoundError as e:
            return {}
            print(f"File not Found :{e}")
    
    @staticmethod
    def write_json(DATABASE,db_type,data):
        filepath = os.path.join(DATABASE["DB_FOLDER"],DATABASE["DB_FILES"][db_type])
        try:
            with ContextManager(filepath,"w") as file:
                json.dump(data,file,indent=4)
            return True

        except Exception as e:
                print(f"An unexpected error occured: {e}")

