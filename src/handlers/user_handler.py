import bcrypt,jwt
from datetime import date, datetime,timedelta,timezone
from fastapi.responses import JSONResponse
from fastapi import Depends
from typing import Annotated
from model.schemas import Token,TokenData
from models import Users
import models
# from movie_booking_fastapi.server import db_dependency,SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES



def create_hash_value(password):
        bytes = password.encode("utf-8")
        # print("bytes", bytes)
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes,salt)
        print("salt",salt)
        # print(hash)
        return hash

def check_user_exist(db,username):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    return bool(user)
        
    

def add_user(db, user):
    user_dict = user.model_dump()
    user_dict['password'] = str(create_hash_value(user_dict['password']))
    user_data = models.Users(**user_dict)
    db.add(user_data)
    db.commit()
    return True

def get_user(db, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def verify_password(plain_password, password_from_db):
    plain_password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes,eval(password_from_db))
    r

    
def authenticate_user(db, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict,ALGORITHM,SECRET_KEY,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_user_member_type(user,member_type):
    if user.permission == member_type:
        return True
    else:
        False
        
# def get_current_user(db:db_dependency, token: Annotated[Users, Depends(oauth2_scheme)]):
#     try:
#         payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
#         username :str = payload.get('sub')
        
#         if username is None:
#             return JSONResponse(status_code=404,content={'detail':"username not found"})
#         token_data = TokenData(username=username)
        
#         # return token_data.username
#     except JWTException as e:
#         return JSONResponse(content={'detail':str(e)})
#     user = get_user(db,token_data.username)
#     if not user:
#         return JSONResponse(status_code=401,content={'detail':'Could not validate Credentials'})
#     return user