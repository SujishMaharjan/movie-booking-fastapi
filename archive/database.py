import json,os
from contextmanager import ContextManager



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

