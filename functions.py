import json,os,bcrypt
from database import *
from main import DATABASE



class Functions:


    @staticmethod
    def input_user_data(user_data_json):
        user_field = ['name','date_of_birth','email','username','password']
        user_details = {}
        for key in user_field:
            value = input(f"Enter your {key}:")
            while key == 'username' and value in user_data_json:
                print("Please Try another username\n")
                value = input(f"Enter your {key}:")
            user_details[key] = value
        
        return user_details

    @staticmethod
    def generate_next_id(user_data_json,key):
        if len(user_data_json) == 0:
            return 0
        print("generated id")
        print(max(sub_dict[key] for _,sub_dict in user_data_json.items()) + 1)
        return max(sub_dict[key] for _,sub_dict in user_data_json.items()) + 1
    
    @staticmethod
    def input_data_from_custom_fields(user_field):
        details_dict = {}
        for key in user_field:
            details_dict[key] = input(f"Enter your {key}:")
        return details_dict
    
    @staticmethod
    def login(DATABASE,db_type,username,password):
        try:
            user_data_json = Database.read_json(DATABASE,db_type)
        except FileNotFoundError as e:
            return {"Error":str(e)}
        
        # print(user_data_json,username,password)
        password_from_db = user_data_json[username]["password"]
        user_password_bytes = password.encode('utf-8')
        result_password = bcrypt.checkpw(user_password_bytes,eval(password_from_db))
        if username in user_data_json and result_password:
        # if username in user_data_json and password == user_data_json[username]["password"]:
            user_details = user_data_json[username]
            # print(user_details,user_details["person_token"])
            return user_details["user_id"]
        else :
            return False
        
    @staticmethod
    def view_movies(DATABASE,db_type):
        movie_data = Database.read_json(DATABASE,db_type)
        available_movies = [sub_dict for movie_name,sub_dict in movie_data.items() if sub_dict["movie_status"] == "Available"]
        filter_details_movies = [
            {
                'movie_name':movie['movie_name'],
                'movie_description':movie['movie_description'],
                'available_seats':movie['available_seats']
            }
            for movie in available_movies
            ]
        for movies in filter_details_movies:
            print(movies)

    @staticmethod
    def check_same_username_with_same_movie(reserve_data,username,movie_name):
        for reserve_key,reserve_sub_dict in reserve_data.items():
            if reserve_sub_dict["username"] == username and reserve_sub_dict["movie_name"] == movie_name:
                return reserve_sub_dict
        return None
    

    @staticmethod
    def validate_token(DATABASE,db_type,token,member_type):
        try:
            relation_data = Database.read_json(DATABASE,"db_relations")
        except FileNotFoundError as e:
            return {"Error": str(e)}

        if token in relation_data  and relation_data[token]["permission"] == member_type:
            return True
        else:
            # print("Error: Invalid Token")
            return False
        
    
    @staticmethod
    def create_hash_value(password):
        bytes = password.encode("utf-8")
        # print("bytes", bytes)
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes,salt)
        print("salt",salt)
        # print(hash)
        return hash

        

    
        

        


