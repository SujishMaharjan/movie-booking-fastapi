import bcrypt
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.auth.exceptions import LoginException
from src.core.log_config import logger

class BcryptPasswordHasher(PasswordHasher):

    def hash_password(self,password):
        logger.debug("Starting hashing for the password")
        try:
            bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(bytes,salt)
            hashed_str = hashed.decode('utf-8')
            logger.debug("Hashing Completed")
            return hashed_str
        except Exception as e:
            logger.error("Error while hashing password: %s", str(e))
            raise RuntimeError("Internal error during password hashing") from e

    
    def verify_password(self,password,hashed):
        logger.debug("Starting hashing for the password")
        try:
            plain_password_bytes = password.encode('utf-8')
            hashed = hashed.encode('utf-8')
            result= bcrypt.checkpw(plain_password_bytes,hashed)
            if not result:
                logger.warning("Password Verification Failed")
                raise LoginException("Invalid Username Or Password")
            logger.debug("Verification Completed")
            return result
        except LoginException:
            raise
        except Exception as e:
            logger.error("Unexpected error occured during verification: %s",str(e))
            raise RuntimeError("Internal error during password verification") from e

        
        

    