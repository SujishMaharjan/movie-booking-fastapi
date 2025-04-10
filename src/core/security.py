import bcrypt,jwt
from datetime import datetime, timezone, timedelta
from src.core.config import SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from src.modules.auth.exceptions import *
from src.core.log_config import logger


def hash_password(password):
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(bytes,salt)
        return hashed_password

def verify_password(plain_password, password_from_db):
    # breakpoint()
    plain_password_bytes = plain_password.encode('utf-8')
    result= bcrypt.checkpw(plain_password_bytes,eval(password_from_db))
    if not result:
        #  logger.debug()
         raise InvalidUsernamePasswordException("Invalid Username Or Password")
    return result


def create_access_token(data: dict):
    breakpoint()
    to_encode = data.copy()
    expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
