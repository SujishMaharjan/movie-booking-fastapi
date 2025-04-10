from src.db_schemas.user import Users
from src.modules.user.exceptions import InvalidMemberTypeException,UserNotFoundException
from src.modules.user.queries import get_all_users
from src.api.entrypoint.user.responses import AllUserResponse




def check_user_member_type(user,member_type):
    if type(user) != Users:
        return False 
    if user.permission != member_type:
        raise InvalidMemberTypeException
    else:
        return True
        

def get_users():
    users = get_all_users()
    if not users:
        raise UserNotFoundException
    all_user_response = [AllUserResponse(**user.model_dump()) for user in users]

    return all_user_response