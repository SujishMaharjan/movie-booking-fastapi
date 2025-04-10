from src.db_schemas.user import Users
from src.modules.user.exceptions import InvalidMemberTypeException,UserNotFoundException
from src.modules.auth.exceptions import InvalidUserNameException, InvalidPasswordException
from src.modules.user.queries import *
from src.api.entrypoint.user.responses import AllUserResponse,UserIdResponse
from src.core.log_config import logger




def check_user_member_type(user,member_type):
    if type(user) != Users:
        return False 
    if user.permission != member_type:
        logger.warning("Trying to access resource- No privileges given to {user.username}")
        raise InvalidMemberTypeException("Permission Denied")
    else:
        return True



def get_users(db):
    users = get_all_users(db)
    if not users:
        raise UserNotFoundException
    all_user_response = [AllUserResponse(**user.__dict__) for user in users]

    return all_user_response

def get_user(db,username):
    user = get_user_from_db_by_username(db,username)
    if not user:
        raise InvalidUserNameException("Invalid username or password")
    return user

def get_user_by_id(db,user_id):
    user = get_user_from_db_by_id(db,user_id)
    if not user:
        raise UserNotFoundException("No such Id")
    return UserIdResponse(**user.__dict__)

# def get_user_by_specific_field(username):
#     column_name = 
#     db.query(Users).filter(Users. == {username}).all()
