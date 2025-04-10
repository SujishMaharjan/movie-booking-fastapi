from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from src.core.exceptions import *
from src.modules.auth.exceptions import *
from src.modules.user.exceptions import *
from src.modules.movie.exceptions import *
from src.modules.reserve.exceptions import *


class CustomExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except DuplicateResourceException as e:
            return JSONResponse(
                status_code=409,
                content={"detail": str(e)}
            )
        except FailedToSaveException as e:
            return JSONResponse(
                status_code=500,
                content={"detail": str(e)}
            )
        except NotFoundException as e:
            return JSONResponse(
                status_code=404,
                content={"detail": str(e)}
            )
        except InvalidInputEnteredException as e:
            return JSONResponse(
                status_code=422,
                content={"detail": str(e)}
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": "An unexpected error occurred"}
            )


# class FailedToSaveException(Exception): ...

# class NotFoundException(Exception): ...

# class InvalidInputEnteredException(Exception): ...