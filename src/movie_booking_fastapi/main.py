import jwt
from fastapi import FastAPI,HTTPException, status, Depends, Request,Form
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated,List
from datetime import date, datetime,timedelta,timezone
from .database.database import engine, SessionLocal, get_db
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from .handlers import movie_handler, user_handler,reserve_handler
from .auth.auth import authenticate_user
from .model import *
from .database import models
from .database.models import Users
from movie_booking_fastapi.logger import *
from decouple import config
from contextlib import asynccontextmanager
import logging
from movie_booking_fastapi.logger import CustomLog,logger
from movie_booking_fastapi.exceptions import UserCreationError,InvalidUserNamePasswordError
from .auth.auth import get_current_user






SECRET_KEY = "00bdd306967a61fdb05237b3adf7e7061de1f80cecddad868435c17123b4b463"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login',scheme_name="JWT")


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Application startup: Logger initialized")
    yield
    logger.info("Application shutdown: Logger closing")

app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(bind=engine)



@app.post('/users/',tags=["users"])
async def create_users(user: UsersBase, db:db_dependency):
    logger.info("users endpoint accessed")

    user = user_handler.create_user(db,user,logger)
    if not user:
        raise UserCreationError
    
    return user

    

@app.post('/login/',tags=["users"]) 
def login_user( db:db_dependency,form_data: OAuth2PasswordRequestForm=Depends()):
    logger.info("login endpoint accessed")

    token = authenticate_user(db,form_data.username,form_data.password)
    if not token:
        raise InvalidUserNamePasswordError
    
    logger.info(f"{form_data.username} logged in")
    return token




@app.post('/movies/',tags=["movies"])
async def add_movies(db:db_dependency,movie :MovieBase, current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("movies endpoint accessed")
    #checks current_user has permission role "admin" as only admin can add movies
    if not user_handler.check_user_member_type(current_user,"admin"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    if movie_handler.check_movie_exist(db,movie.movie_name):
        return JSONResponse(status_code=409, content={'detail':'Movie already exist'})
    if not movie_handler.add_movie(db,movie):
        return JSONResponse(content={'detail':"Error in adding movies"})
    logger.info(f"{movie.movie_name} added by {current_user.username}")
    return MovieResponse(**movie.model_dump())
    
 
@app.get('/movies/',tags=["movies"])
async def show_available_movies(db:db_dependency):
    logger.info("movies endpoint accessed")
    movies = movie_handler.get_all_movies_available(db)
    return movies


@app.post('/reserve/',tags=["Reserves"])
async def reserve_movies(db:db_dependency,reserve:ReserveBase,current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("Reserve endpoint accessed")
    if not user_handler.check_user_member_type(current_user,"member"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    if not movie_handler.check_movie_available(db,reserve.movie_name):
        return JSONResponse(status_code=404, content={'detail':'Movie Not Available'})
    if not reserve_handler.check_valid_seats_to_reserve(db,reserve):
        return JSONResponse(content={'detail':f"Invalid seats entered"})
    if not reserve_handler.add_reservation(db,reserve,current_user):
        return JSONResponse(content={'detail':"Error in reserving movies"})
    logger.info(f"{reserve.movie_name} reserved by {current_user.username}")
    return {"username":current_user.username,"movie_name":reserve.movie_name,"reserved_seats":reserve.no_of_seats}


@app.get('/reserve/',tags=["Reserves"])
async def show_reserve(db:db_dependency,current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("Reserve endpoint accessed")
    if not user_handler.check_user_member_type(current_user,"member"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    return reserve_handler.get_all_reserves(db,current_user)

  
    

@app.put('/reserve/',tags=["Reserves"])
async def unreserve_movies(db:db_dependency,reserve:ReserveBase,current_user:Annotated[Users, Depends(get_current_user)]):
    logger.info("Reserve endpoint accessed")
    if not user_handler.check_user_member_type(current_user,"member"):
        return JSONResponse(status_code=401,content={'detail':"Unauthorized User"})
    db_reserve = reserve_handler.get_reserve_from_db(db,current_user,reserve.movie_name)
    if not db_reserve:
        return JSONResponse(status_code=404, content={'detail':f'No Reservations done in {reserve.movie_name} found by {current_user.username}'})
    before_reserve_seats = db_reserve.user_reserve_seats
    if not reserve_handler.check_valid_seats_to_unreserve(db,db_reserve,reserve.no_of_seats):
        JSONResponse(content={'detail':f"Invalid seats entered, Reserved  Seats: {db_reserve.user_reserve_seats}"})
    if not reserve_handler.unreserve_seats(db,db_reserve,reserve.no_of_seats,current_user):
        return JSONResponse(content={'detail':"Error in reserving movies"})
    logger.info(f"{reserve.movie_name} reserved by {current_user.username}")
    return UnReserveResponse(username=current_user.username,movie_name=reserve.movie_name,before_reserve_seats=before_reserve_seats,update_reserve_seats=db_reserve.user_reserve_seats)



                        
                        