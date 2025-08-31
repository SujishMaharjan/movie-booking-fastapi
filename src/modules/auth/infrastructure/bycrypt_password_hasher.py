import bcrypt
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.auth.exceptions import LoginException

class BcryptPasswordHasher(PasswordHasher):

    def hash_password(self,password):
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes,salt)
        hashed_str = hashed.decode('utf-8')
        return hashed_str
    
    def verify_password(self,password,hashed):
        plain_password_bytes = password.encode('utf-8')
        hashed = hashed.encode('utf-8')
        result= bcrypt.checkpw(plain_password_bytes,hashed)
        if not result:
            #  logger.warning()
                raise LoginException("Invalid Username Or Password")
        return result


        
        

    