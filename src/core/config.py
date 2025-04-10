from decouple import config
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = config("secret")
ALGORITHM = config("algorithm")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("access_token_expiree_miutes"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/signin',scheme_name="JWT")


