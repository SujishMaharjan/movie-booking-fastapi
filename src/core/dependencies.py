from typing import Annotated,Any
from src.config.settings import JwtSettings,HallSettings
from fastapi import Depends,Request
from src.core.provider import Provider
from src.modules.user.entity.user import User
# from src.core.security import get_current_user
from src.core.database import get_db_session
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
from src.modules.auth.infrastructure.bycrypt_password_hasher import BcryptPasswordHasher
from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.reserve.infrastructure.postgres_reserve_repository import PostgresReserveRepository
from sqlalchemy.orm import Session
from src.core.security import oauth2_scheme
from src.core.exceptions import NotFoundException



def get_jwt_settings(request: Request):
    return request.app.state.settings.jwt

def get_hall_settings(request: Request):
    return request.app.state.settings.hall

# def get_provider(request: Request)->Provider:
#     return Provider(request)

# def get_user_repo(
#         db_session:Session=Depends(get_db_session)
# ):
#     return PostgresUserRepository(db_session)

# def get_token_repo(
#         token_repo: Annotated[TokenRepository,Depends()],
#         jwt_settings:Session=Depends(get_jwt_settings)
# ):
#     return JwtService(jwt_settings)

# def get_password_hasher_repo(
#         hasher_repository: Annotated[PasswordHasher,Depends()],
# ):
#     return BcryptPasswordHasher()

# def get_movie_repo(
#         movie_repo: Annotated[MovieRepository,Depends()],
#         db_session:Session=Depends(get_db_session)
# ):
#     return movie_repo(db_session)

# def get_reserve_repo(
#         resreve_repo: Annotated[ReserveRepository,Depends()],
#         db_session:Session=Depends(get_db_session)
# ):
#     return resreve_repo(db_session)

def get_provider(
        JwtSettings: JwtSettings=Depends(get_jwt_settings),
        db_session: Session= Depends(get_db_session)
        
        # user_repository:UserRepository= Depends(get_user_repo),
        # token_repository:TokenRepository= Depends(get_token_repo),
        # password_hasher_repository:PasswordHasher= Depends(get_password_hasher_repo),
        # movie_repository:MovieRepository= Depends(get_movie_repo),
        # reserve_repository:ReserveRepository= Depends(get_reserve_repo)      
):
    
    return Provider(
        db_session=db_session,
        user_repository=PostgresUserRepository(db_session),
        token_repository=JwtService(JwtSettings),
        password_hasher_repository=BcryptPasswordHasher(),
        movie_repository=PostgresMovieRepository(db_session),
        reserve_repository=PostgresReserveRepository(db_session)
    )

def get_current_user(
        provider: Annotated[Any,Depends(get_provider)],
        token:Annotated[str,Depends(oauth2_scheme)]
):
    
    token_repo=provider.token_repository
    user_repo=provider.user_repository
    username=token_repo.validate_and_decode_token(token).get("sub")
    raw_user = user_repo.get_by_username(username)
    if not raw_user:
        raise NotFoundException("User Not Found")
    user = user_repo.to_dataclass(raw_user,User)
    return user

    


AnnotatedCurrentUser = Annotated[User,Depends(get_current_user)]
AnnotatedRepositoryProvider = Annotated[Any,Depends(get_provider)]
AnnotatedJwtSettings = Annotated[JwtSettings,Depends(get_jwt_settings)]
AnnotatedHallSettings = Annotated[HallSettings,Depends(get_hall_settings)]

