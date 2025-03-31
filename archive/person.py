from enum import StrEnum
from database.database import Database
import uuid
from functions import Functions
from datetime import date
import os

class Membertype(StrEnum):
    admin = "admin"
    member = "member"


#creating class person
class Person:

    def __init__(self,user_id:str,name:str,date_of_birth:str,email:str,username:str,password:str,permission):
        self._user_id = user_id
        self._name = name
        self._date_of_birth = date_of_birth
        self._email = email
        self._username = username
        self._password = password
        self._permission = permission
        
    
    def add_person(self,DATABASE,db_type):
        # loading the existing data
        json_data = Database.read_json(DATABASE,db_type)

        #getting the data to modify in existing data
        user_dict = self.__dict__

        #removing the leading _ in key
        cleaned_dict = {key.lstrip('_'): value for key, value in user_dict.items()}

        json_data[self._username] = cleaned_dict
        if Database.write_json(DATABASE,db_type,json_data):
            return self._user_id
        else:
            return None
        
    def add_relation(self,DATABASE,db_type,token,permission):
        relation_data_json = Database.read_json(DATABASE,db_type)
        data = {
            "person_token": token,
            "permission" : permission
        }
        relation_data_json[token] = data
        print(relation_data_json)
        Database.write_json(DATABASE,db_type,relation_data_json)
        print(f"Relation created for token with Member_type")

    @property
    def user_id(self):
        return self._user_id
    
    @property
    def person_token(self):
        return self._person_token
    
    @property
    def username(self):
        return self._username
    
    @property
    def permission(self):
        return self._permission
    
   
    # def get_permission(self):
    #     return self._permission
    def __repr__(self):
        return {"user_id":self._user_id,"name":self._name,"date_of_birth":self._date_of_birth,"email":self._email,"username":self._username,"password":self._password,"permission":self._permission}
        



class Admin(Person):

    def __init__(self, user_id, name, date_of_birth, email, username, password, permission="admin"):
        super().__init__(user_id, name, date_of_birth, email, username, password, permission)

    def add_movies():
        pass


class Member(Person):

    def __init__(self, user_id, name, date_of_birth, email, username, password, permission="member"):
        super().__init__(user_id, name, date_of_birth, email, username, password, permission)

    def reserve_movies():
        pass

    def unreserve_movies():
        pass