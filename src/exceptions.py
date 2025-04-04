from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from .log import logger


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found"):
        logger.exception(f"{detail}",exc_info=True)
        super().__init__(status_code=404, detail=detail)


class UserExistError(HTTPException):
    def __init__(self,detail: str="Username already exist"):
        logger.error(f"{detail}")
        super().__init__(status_code=409, detail=detail)

class UserCreationError(HTTPException):
    def __init__(self, detail: str ="An Unexpected Error while creating user"):
        logger.error(f"{detail}")
        super().__init__(status_code=500, detail= detail)

class InvalidUserNamePasswordError(HTTPException):
    def __init__(self, detail: str="Invalid Username or Password"):
        logger.error(f"{detail}")
        super().__init__(status_code=401, detail= detail)




class MemberTypeError(HTTPException):
    def __init__(self, detail: str="Unauthorized User"):
        logger.error(f"{detail}")
        super().__init__(status_code=401, detail= detail)

class MovieExistError(HTTPException):
    def __init__(self, detail: str="Movie already exist"):
        logger.error(f"{detail}")
        super().__init__(status_code=409, detail= detail)

class MovieNotAvailableError(HTTPException):
    def __init__(self, detail: str="Movie Not Available"):
        logger.error(f"{detail}")
        super().__init__(status_code=404, detail= detail)

class FailedToAddMovieError(HTTPException):
    def __init__(self, detail: str ="An Unexpected Error while adding movies"):
        logger.error(f"{detail}")
        super().__init__(status_code=500, detail= detail)

class FailedToReserveError(HTTPException):
     def __init__(self, detail: str ="An Unexpected Error while reserving movies"):
        logger.error(f"{detail}")
        super().__init__(status_code=500, detail= detail)

class InvalidSeatsEnteredError(HTTPException):
    def __init__(self, detail: str ="Invalid seats entered"):
        logger.error(f"{detail}")
        super().__init__(status_code=400, detail= detail)

    
class MovieNotReserveByUserError(HTTPException):
    def __init__(self, detail: str):
        logger.error(f"{detail}")
        super().__init__(status_code=404, detail= detail)



# def raise_not_found_exception(detial: str = "Resource not found"):
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=detail)


# class UserAlreadyExist(Exception):
#     raise JSONResponse(status_code=409, content={'detail':'Username already exist'})
