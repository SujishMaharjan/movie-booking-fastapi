import jwt
from fastapi import FastAPI,HTTPException, status, Depends, Request,Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated,List
from datetime import date, datetime,timedelta,timezone
from database.database import engine, SessionLocal, get_db
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from handlers import movie_handler, user_handler,reserve_handler
from model.schemas import *
import models
from models import Users



SECRET_KEY = "00bdd306967a61fdb05237b3adf7e7061de1f80cecddad868435c17123b4b463"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login',scheme_name="JWT")


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

@app.post('/users/',tags=["users"])
async def create_users(user: UsersBase, db:db_dependency):
    # breakpoint()
    if user_handler.check_user_exist(db,user.username):
        return JSONResponse(status_code=409, content={'detail':'Username already exist'})
    if user_handler.add_user(db,user):
        return UserResponse(**user.model_dump())
    
    

@app.post('/login/',tags=["users"]) 
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
        # breakpoint()
        # return token_data.username
    except InvalidTokenError:
        return JSONResponse(content={'detail':"Invalid Token"})
    user = user_handler.get_user(db,token_data.username)
    if not user:
        return JSONResponse(status_code=401,content={'detail':'Could not validate Credentials'})
    return user

@app.post('/movies/',tags=["movies"])
async def add_movies(db:db_dependency,movie :MovieBase, current_user:Annotated[Users, Depends(get_current_user)]):
    #checks current_user has permission role "admin" as only admin can add movies
    # breakpoint()
    if not user_handler.check_user_member_type(current_user,"admin"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    # checks if there is same movie exist 
    if movie_handler.check_movie_exist(db,movie.movie_name):
        return JSONResponse(status_code=409, content={'detail':'Movie already exist'})
    if movie_handler.add_movie(db,movie):
        return MovieResponse(**movie.model_dump())
    
 
@app.get('/movies/',tags=["movies"])
async def show_available_movies(db:db_dependency):
    movies = movie_handler.get_all_movies_available(db)
    return movies


@app.post('/reserve/',tags=["Reserves"])
def reserve_movies(db:db_dependency,reserve:ReserveBase,current_user:Annotated[Users, Depends(get_current_user)]):
    # breakpoint()
    if not user_handler.check_user_member_type(current_user,"member"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    # movie = movie_handler.check_movie_available(reserve.movie_name, movies=Depends(show_available_movies))
    if not movie_handler.check_movie_available(db,reserve.movie_name):
        return JSONResponse(status_code=404, content={'detail':'Movie Not Available'})
    if not reserve_handler.add_reservation(db,reserve,current_user):
        return JSONResponse(content={'detail':"Error in reserving movies"})
    return ReserveResponse(**reserve.model_dump(),username=current_user.username)




@app.get('/reserve/',tags=["Reserves"])
def show_reserve(db:db_dependency,current_user:Annotated[Users, Depends(get_current_user)]):
    if not user_handler.check_user_member_type(current_user,"member"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    reserves = reserve_handler.get_all_reserves(db,current_user)
    return reserves

  


    
    

@app.put('/reserve/')
def unreserve_movies(db:db_dependency,reserve:ReserveBase,current_user:Annotated[Users, Depends(get_current_user)]):
    # #get token from headers
    # auth_header = request.headers.get("Authorization")
    # if not auth_header or not auth_header.startswith("Bearer"):
    #     print("No token recieved")
    #     raise HTTPException(status_code=401, detail="Unauthorized: No token received!")
    
    # token = auth_header.split(" ")[1]

    # if Functions.validate_token(DATABASE,"db_relation",token,"member"):

    #     # user_data = Database.read_json(DATABASE,'db_users')
    #     # # print(user_data)
    #     # user_details = user_data[reserve.username]
    #     # # print(user_details)

    #     movie_data = Database.read_json(DATABASE,'db_movies')
    #     if reserve.movie_name not in movie_data:
    #         return "Error:No such Movie"
    #     movie_details = movie_data[reserve.movie_name]
    #     m = Movie(**movie_details)
    #     if reserve.no_of_seats <= m.booked_seats:
    #         pass
    #     else:    
    #         return {"Error": f"Seats to unreserved greater than {m.booked_seats} reserved seats"}


    #     reserve_data = Database.read_json(DATABASE,'db_reserves')
    #     if reserve.reserve_id not in reserve_data:
    #         return {"Error": "No such reserve_id"}

    #     reserve_details= reserve_data[reserve.reserve_id]

    #     r = Reservation(**reserve_details)
    #     if r.unreserve_seats(DATABASE,"db_reserves",reserve.no_of_seats):
    #          if m.update_booked_seats(DATABASE,"db_movies",0,reserve.no_of_seats):
    #             return {'reserve_id':reserve.reserve_id,'username':reserve.username,'movie_name':reserve.movie_name,'booked_seats':r.booked_seats,'message':"Successfully UnReserved seats"}
    #     else:
    #         return {"Error":"Failed to Unreserved booked seats"}

             
    # else:
    #     return {"Error":"Invalid Token"}
 

                        
                        