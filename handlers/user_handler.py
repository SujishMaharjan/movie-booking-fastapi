import models,bcrypt,jwt
from datetime import date, datetime,timedelta,timezone
from fastapi.responses import JSONResponse
from fastapi import Depends
from typing import Annotated
from model.schemas import Token,TokenData
from models import Users
from jwt.exceptions import InvalidTokenError

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
    return user

def add_user(db, user):
    user_dict = user.model_dump()
    user_dict['password'] = str(create_hash_value(user_dict['password']))
    user_data = models.Users(**user_dict)
    db.add(user_data)
    db.commit()
    return True

def get_user(db, username: str):
    return db.query(models.Users).filter(models.Users.username == username).one()

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

# def get_current_user(db:db_dependency, token: Annotated[Users, Depends(oauth2_scheme)]):
#     credentials_exception = JSONResponse(
#         status_code=401,
#         content={
#             "detail":"Could not validate credentials"
#         }
#     )
#     # breakpoint()
#     try:
#         payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
#         username :str = payload.get('sub')
#         # breakpoint()
#         if username is None:
#             return JSONResponse(status_code=404,content={'detail':"username not found"})
#         token_data = TokenData(username=username)
#         # return token_data.username
#     except InvalidTokenError:
#         return JSONResponse(content={'detail':"Invalid Token"})
#     user = get_user(db,token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: Annotated[Users, Depends(get_current_user)]):
#     # breakpoint()
#     if current_user.disabled:
#         return JSONResponse(status_code=400,content={'detail':'Inactive user'})
#     return current_user
    

def check_user_member_type(user,member_type):
    if user.permission == member_type:
        return user.permission