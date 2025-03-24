import os,json,bcrypt
from person import *
from reserve import Reservation
from movie import Movie
from database import Database
from contextmanager import ContextManager
from fastapi import FastAPI,HTTPException, status, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, SecretStr
from enum import StrEnum
from typing import Optional,Annotated
from datetime import date, datetime


DATABASE = {
    "DB_FOLDER" : "Database",
    "DB_FILES" : {
        "db_users": "user.json",
        "db_movies":"movie.json",
        "db_reserves":"reserve.json",
        "db_relations":"relation.json"
    }
}



class MemberType(StrEnum):
    admin = "admin"
    member = "member"

class AvailableType(StrEnum):
    available = "Available"
    unavailable = "Unavailable"
    fully_reserved = "Fully Reserved"



class Users(BaseModel):
    name: str
    date_of_birth : str
    email : str
    username : str
    password : str
    permission : MemberType
    user_id : Optional[str] = None

class MovieModel(BaseModel):
    movie_name: str
    movie_status : AvailableType
    movie_description : str
    movie_id : Optional[str] = None

class ReserveModel(BaseModel):
    username: str
    movie_name: str
    no_of_seats: int
    reserve_id: Optional[str] = None


app = FastAPI()

@app.post('/users/')
def create_users(users: Users):
    """
    Creates a new user account.

    - **users (Users)**: A Pydantic model containing user details, including username, password, and permission level.
    - **Database Initialization**: Ensures the database is set up before storing user data.
    - **User ID Generation**: Assigns a unique ID to the new user.
    - **Password Hashing**: Encrypts the password for security.
    - **User Verification**: Checks if the username is already in use.
    - **Role Assignment**: Creates an Admin or Member user based on the provided permission.
    - **Token Generation**: Adds the user and their role to the database.
    
    **Responses:**
    - ✅ **201 Created**: Returns a success message and user details if the account is created.
    - ❌ **400 Bad Request**: Returns an error message if the username is already taken.

    **Returns:**
    - A dictionary containing the username, permission, and a success message.
    - If the username already exists, returns an error message.

    """
    Database.create_database(DATABASE)
    u = users.model_dump()
    u["user_id"] = str(uuid.uuid1())
    u['password'] = str(Functions.create_hash_value(u['password']))

    user_data_json = Database.read_json(DATABASE,"db_users")

    if u["username"] not in user_data_json:
        p = Admin(**u) if u["permission"] == "admin" else Member(**u) 
        token = p.add_person(DATABASE,"db_users")
        p.add_relation(DATABASE,"db_relations",token,p.permission)
        response = {key : value for key, value in u.items() if key  in ["username","permission"]}
        response['message'] ="User added successfully"
        return response
    else:
        return {"error":"Please try another username"}
    

@app.post('/login/') 
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):

    token= Functions.login(DATABASE,"db_users",form_data.username,form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate":"Bearer"})
    else:
         return {"token":token}


@app.post('/movies/')
def add_movies(movie :MovieModel, request:Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        print("No token recieved")
        raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
    token = auth_header.split(" ")[1]

    if Functions.validate_token(DATABASE,"db_relation",token,"admin"):
        movie_data = Database.read_json(DATABASE,'db_movies')
        if movie.movie_name in movie_data:
            return {"Error":f"Movie {movie.movie_name}already in database"}

        movie_dict = movie.model_dump()
        movie_dict["movie_id"] = str(uuid.uuid4())
        movie_dict["movie_status"] = "Available"

        m = Movie(**movie_dict)
        movie_id = m.add_movie(DATABASE,"db_movies")
        if not movie_id:
            return {"Error: An Unexpected error occured when adding movies"}
        return {**movie_dict,"message":"Movie added Successfully","movie_id": movie_id}
        
    else:
        return {"Invalid token"}
    
@app.get('/movies/')
def show_available_movies():
    movies_list = Database.read_json(DATABASE,"db_movies")
   
    filtered_movie_list = {
        movie["movie_id"]:{
            "movie_id":movie["movie_id"],
            "movie_name":movie["movie_name"],
            "movie_status":movie["movie_status"],
            "movie_description":movie["movie_description"],
            "available_seats":movie["available_seats"]
        }
        for _,movie in movies_list.items() if movie["movie_status"] == "Available"}
    # print(filtered_movie_list)
    return filtered_movie_list


@app.post('/reserve/')
def reserve_movies(reserve:ReserveModel,request:Request):
    #get token from headers
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        print("No token recieved")
        raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
    token = auth_header.split(" ")[1]

    if Functions.validate_token(DATABASE,"db_relation",token,"member"):

        user_data = Database.read_json(DATABASE,'db_users')
        # print(user_data)
        if reserve.username not in user_data:
            return {"Error":"No such username"}
        user_details = user_data[reserve.username]
        # print(user_details)

        movie_data = Database.read_json(DATABASE,'db_movies')
        if reserve.movie_name not in movie_data:
            raise KeyError("Error:No such Movie")
        movie_details = movie_data[reserve.movie_name]
            
        m = Movie(**movie_details)
        if reserve.no_of_seats <= m.available_seats:
            pass
        else:    
            return {"Error": f"Seats to reserved greater than {m.available_seats} available seats"}

        reserve_dict = {}
        reserve_dict["reserve_id"] = str(uuid.uuid4())
        reserve_dict["user_id"] = user_details["user_id"]
        reserve_dict["username"] = user_details["username"]
        reserve_dict["movie_id"] = movie_details["movie_id"]
        reserve_dict["movie_name"] = movie_details["movie_name"]
        reserve_dict["booked_seats"] = reserve.no_of_seats
        

        
        reserve_data = Database.read_json(DATABASE,'db_reserves')
        reserve_details= Functions.check_same_username_with_same_movie(reserve_data,reserve.username,reserve.movie_name)
        print(reserve_details)
        if m.update_booked_seats(DATABASE,"db_movies",reserve.no_of_seats,0):
            if reserve_details:
                print("hello reserve_details")
                r = Reservation(**reserve_details)
                r.booked_seats = r.booked_seats + reserve.no_of_seats
            else:
                r = Reservation(**reserve_dict)
            reserve_id = r.reserve_seats(DATABASE,"db_reserves")
            
            return {'reserve_id':reserve_id,'username':reserve.username,'movie_name':reserve.movie_name,'booked_seats':r.booked_seats,'message':"Successfully Reserved seats"}
        else:
            return {"Error":"Failed to update booked seats"}

        
    else:
        return {"Error":"Invalid Token"}
    


@app.get('/reserve/{username}')
def show_reserve_by_user_name(username:str,request:Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        print("No token recieved")
        raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
    token = auth_header.split(" ")[1]

    if Functions.validate_token(DATABASE,"db_relation",token,"member"):
            reserve_data = Database.read_json(DATABASE,'db_reserves')
            filtered_reserve_data = {
                            reserve["reserve_id"]:{
                                "reserve_id":reserve["reserve_id"],
                                "username":reserve["username"],
                                "movie_name":reserve["movie_name"],
                                "reserve_seat":reserve["booked_seats"]   
                            }
                            for _,reserve in reserve_data.items() if reserve["username"]==username}

            return filtered_reserve_data
    else:
        return "Error: Invalid Token"


    
    

@app.put('/reserve/')
def unreserve_movies(reserve:ReserveModel,request:Request):
    #get token from headers
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer"):
        print("No token recieved")
        raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
    token = auth_header.split(" ")[1]

    if Functions.validate_token(DATABASE,"db_relation",token,"member"):

        # user_data = Database.read_json(DATABASE,'db_users')
        # # print(user_data)
        # user_details = user_data[reserve.username]
        # # print(user_details)

        movie_data = Database.read_json(DATABASE,'db_movies')
        if reserve.movie_name not in movie_data:
            return "Error:No such Movie"
        movie_details = movie_data[reserve.movie_name]
        m = Movie(**movie_details)
        if reserve.no_of_seats <= m.booked_seats:
            pass
        else:    
            return {"Error": f"Seats to unreserved greater than {m.booked_seats} reserved seats"}


        reserve_data = Database.read_json(DATABASE,'db_reserves')
        if reserve.reserve_id not in reserve_data:
            return {"Error": "No such reserve_id"}

        reserve_details= reserve_data[reserve.reserve_id]

        r = Reservation(**reserve_details)
        if r.unreserve_seats(DATABASE,"db_reserves",reserve.no_of_seats):
             if m.update_booked_seats(DATABASE,"db_movies",0,reserve.no_of_seats):
                return {'reserve_id':reserve.reserve_id,'username':reserve.username,'movie_name':reserve.movie_name,'booked_seats':r.booked_seats,'message':"Successfully UnReserved seats"}
        else:
            return {"Error":"Failed to Unreserved booked seats"}

             
    else:
        return {"Error":"Invalid Token"}
 

                        
                        