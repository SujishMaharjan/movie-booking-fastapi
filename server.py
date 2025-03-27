import jwt
from archive.person import *
from archive.reserve import Reservation
from archive.movie import Movie
from database import Database
from archive.contextmanager import ContextManager
from fastapi import FastAPI,HTTPException, status, Depends, Request,Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated,List
from datetime import date, datetime,timedelta,timezone
from database import engine, SessionLocal, get_db
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from handlers import user_handler,movie_handlers
from schemas import *
import models
from models import Users



SECRET_KEY = "00bdd306967a61fdb05237b3adf7e7061de1f80cecddad868435c17123b4b463"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login',scheme_name="JWT")


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post('/users/')
async def create_users(user: UsersBase, db:db_dependency):
    # breakpoint()
    if user_handler.check_user_exist(db,user.username):
        return JSONResponse(status_code=409, content={'detail':'Username already exist'})
    if user_handler.add_user(db,user):
        return UserResponse(**user.model_dump())
    
    

@app.post('/login/') 
def login_user( db:db_dependency,form_data: OAuth2PasswordRequestForm=Depends()):
    user = user_handler.authenticate_user(db,form_data.username,form_data.password)
    if not user:
        return JSONResponse(status_code=401,content={'detail':'Incorrect username or password'})
    access_token = user_handler.create_access_token(
        data={'sub':user.username},
        ALGORITHM=ALGORITHM,
        SECRET_KEY=SECRET_KEY,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token,token_type='bearer')
    

def get_current_user(db:db_dependency, token: Annotated[Users, Depends(oauth2_scheme)]):
    credentials_exception = JSONResponse(
        status_code=401,
        content={
            "detail":"Could not validate credentials"
        }
    )
    # breakpoint()
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username :str = payload.get('sub')
        # breakpoint()
        if username is None:
            return JSONResponse(status_code=404,content={'detail':"username not found"})
        token_data = TokenData(username=username)
        # return token_data.username
    except InvalidTokenError:
        return JSONResponse(content={'detail':"Invalid Token"})
    user = user_handler.get_user(db,token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post('/movies/')
async def add_movies(db:db_dependency,movie :MovieBase, current_user:Annotated[Users, Depends(get_current_user)]):
    #checks current_user has permission role "admin" as only admin can add movies
    if not user_handler.check_user_member_type(current_user,"admin"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    # checks if there is same movie exist 
    if movie_handlers.check_movie_exist(db,movie.movie_name):
        return JSONResponse(status_code=409, content={'detail':'Movie already exist'})
    if movie_handlers.add_movie(db,movie):
        return MovieResponse(**movie.model_dump())
    
 
# @app.get('/movies/')
# def show_available_movies():
#     movies_list = Database.read_json(DATABASE,"db_movies")
   
#     filtered_movie_list = {
#         movie["movie_id"]:{
#             "movie_id":movie["movie_id"],
#             "movie_name":movie["movie_name"],
#             "movie_status":movie["movie_status"],
#             "movie_description":movie["movie_description"],
#             "available_seats":movie["available_seats"]
#         }
#         for _,movie in movies_list.items() if movie["movie_status"] == "Available"}
#     # print(filtered_movie_list)
#     return filtered_movie_list


# @app.post('/reserve/')
# def reserve_movies(reserve:ReserveBase,request:Request):
#     #get token from headers
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer"):
#         print("No token recieved")
#         raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
#     token = auth_header.split(" ")[1]

#     if Functions.validate_token(DATABASE,"db_relation",token,"member"):

#         user_data = Database.read_json(DATABASE,'db_users')
#         # print(user_data)
#         if reserve.username not in user_data:
#             return {"Error":"No such username"}
#         user_details = user_data[reserve.username]
#         # print(user_details)

#         movie_data = Database.read_json(DATABASE,'db_movies')
#         if reserve.movie_name not in movie_data:
#             raise KeyError("Error:No such Movie")
#         movie_details = movie_data[reserve.movie_name]
            
#         m = Movie(**movie_details)
#         if reserve.no_of_seats <= m.available_seats:
#             pass
#         else:    
#             return {"Error": f"Seats to reserved greater than {m.available_seats} available seats"}

#         reserve_dict = {}
#         reserve_dict["reserve_id"] = str(uuid.uuid4())
#         reserve_dict["user_id"] = user_details["user_id"]
#         reserve_dict["username"] = user_details["username"]
#         reserve_dict["movie_id"] = movie_details["movie_id"]
#         reserve_dict["movie_name"] = movie_details["movie_name"]
#         reserve_dict["booked_seats"] = reserve.no_of_seats
        

        
#         reserve_data = Database.read_json(DATABASE,'db_reserves')
#         reserve_details= Functions.check_same_username_with_same_movie(reserve_data,reserve.username,reserve.movie_name)
#         print(reserve_details)
#         if m.update_booked_seats(DATABASE,"db_movies",reserve.no_of_seats,0):
#             if reserve_details:
#                 print("hello reserve_details")
#                 r = Reservation(**reserve_details)
#                 r.booked_seats = r.booked_seats + reserve.no_of_seats
#             else:
#                 r = Reservation(**reserve_dict)
#             reserve_id = r.reserve_seats(DATABASE,"db_reserves")
            
#             return {'reserve_id':reserve_id,'username':reserve.username,'movie_name':reserve.movie_name,'booked_seats':r.booked_seats,'message':"Successfully Reserved seats"}
#         else:
#             return {"Error":"Failed to update booked seats"}

        
#     else:
#         return {"Error":"Invalid Token"}
    


# @app.get('/reserve/{username}')
# def show_reserve_by_user_name(username:str,request:Request):
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer"):
#         print("No token recieved")
#         raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
#     token = auth_header.split(" ")[1]

#     if Functions.validate_token(DATABASE,"db_relation",token,"member"):
#             reserve_data = Database.read_json(DATABASE,'db_reserves')
#             filtered_reserve_data = {
#                             reserve["reserve_id"]:{
#                                 "reserve_id":reserve["reserve_id"],
#                                 "username":reserve["username"],
#                                 "movie_name":reserve["movie_name"],
#                                 "reserve_seat":reserve["booked_seats"]   
#                             }
#                             for _,reserve in reserve_data.items() if reserve["username"]==username}

#             return filtered_reserve_data
#     else:
#         return "Error: Invalid Token"


    
    

# @app.put('/reserve/')
# def unreserve_movies(reserve:ReserveBase,request:Request):
#     #get token from headers
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer"):
#         print("No token recieved")
#         raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
#     token = auth_header.split(" ")[1]

#     if Functions.validate_token(DATABASE,"db_relation",token,"member"):

#         # user_data = Database.read_json(DATABASE,'db_users')
#         # # print(user_data)
#         # user_details = user_data[reserve.username]
#         # # print(user_details)

#         movie_data = Database.read_json(DATABASE,'db_movies')
#         if reserve.movie_name not in movie_data:
#             return "Error:No such Movie"
#         movie_details = movie_data[reserve.movie_name]
#         m = Movie(**movie_details)
#         if reserve.no_of_seats <= m.booked_seats:
#             pass
#         else:    
#             return {"Error": f"Seats to unreserved greater than {m.booked_seats} reserved seats"}


#         reserve_data = Database.read_json(DATABASE,'db_reserves')
#         if reserve.reserve_id not in reserve_data:
#             return {"Error": "No such reserve_id"}

#         reserve_details= reserve_data[reserve.reserve_id]

#         r = Reservation(**reserve_details)
#         if r.unreserve_seats(DATABASE,"db_reserves",reserve.no_of_seats):
#              if m.update_booked_seats(DATABASE,"db_movies",0,reserve.no_of_seats):
#                 return {'reserve_id':reserve.reserve_id,'username':reserve.username,'movie_name':reserve.movie_name,'booked_seats':r.booked_seats,'message':"Successfully UnReserved seats"}
#         else:
#             return {"Error":"Failed to Unreserved booked seats"}

             
#     else:
#         return {"Error":"Invalid Token"}
 

                        
                        