import bcrypt
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.auth.exceptions import LoginException

class BcryptPasswordHasher(PasswordHasher):

    def hash_password(self,password):
        bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(bytes,salt)
        return hashed
    
    def verify_password(self,password, hashed_password):
        plain_password_bytes = password.encode('utf-8')
        if result:= bcrypt.checkpw(plain_password_bytes,eval(hashed_password)):
            #  logger.warning()
                raise LoginException("Invalid Username Or Password")
        return result


        
        

    