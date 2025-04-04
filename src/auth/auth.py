import bcrypt,jwt
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.responses import JSONResponse
from ..database.database import get_db
from ..handlers.user_handler import get_user
from jwt.exceptions import InvalidTokenError
from ..model.token import Token, TokenData
from ..exceptions import InvalidUserNamePasswordError
from decouple import config




# SECRET_KEY = config("secret")
# ALGORITHM = config("algorithm")
# ACCESS_TOKEN_EXPIRE_MINUTES = config("access_token_expiree_miutes")
SECRET_KEY="00bdd306967a61fdb05237b3adf7e7061de1f80cecddad868435c17123b4b463"
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login',scheme_name="JWT")

def create_hash_value(password):
        bytes = password.encode("utf-8")
        # print("bytes", bytes)
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes,salt)
        
        return hash

def verify_password(plain_password, password_from_db):
    plain_password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes,eval(password_from_db))
    


def create_access_token(data: dict,ALGORITHM,SECRET_KEY,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def get_current_user(db:Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        username :str = payload.get('sub')
        
        if username is None:
            return JSONResponse(status_code=404,content={'detail':"username not found"})
        token_data = TokenData(username=username)
        
        # return token_data.username
    except InvalidTokenError :
        return JSONResponse(content={'detail':'Invalid key'})
    user = get_user(db,token_data.username)
    if not user:
        return JSONResponse(status_code=401,content={'detail':'Could not validate Credentials'})
    return user


def authenticate_user(db,username,password):
    user = get_user(db, username)
    if not user or  not verify_password(password, user.password):
        raise InvalidUserNamePasswordError
    access_token = create_access_token(
        data={'sub':username},
        ALGORITHM=ALGORITHM,
        SECRET_KEY=SECRET_KEY,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=access_token,token_type='bearer')
