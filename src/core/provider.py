from fastapi import Depends
from src.core.database import get_db_session
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from src.modules.reserve.infrastructure.postgres_reserve_repository import PostgresReserveRepository
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
from src.modules.auth.infrastructure.bycrypt_password_hasher import BcryptPasswordHasher
from src.core.database import get_db_session
from fastapi import Request




class Provider:
    def __init__(self,request:Request):

        self.jwt_settings = request.app.state.settings.jwt
        self.db_session = next(get_db_session(request))
        self.token_repository:TokenRepository = JwtService(self.jwt_settings)
        self.user_repository:UserRepository = PostgresUserRepository(self.db_session)
        self.movie_repository:MovieRepository = PostgresMovieRepository(self.db_session)
        self.reserve_repository:ReserveRepository = PostgresReserveRepository(self.db_session)
        self.hasher_repository:PasswordHasher = BcryptPasswordHasher()

    # @property
    # def token_repository(self):
    #     return self.token_repository
    
    # @property
    # def user_repository(self):
    #     return self.user_repository
    
    # @property
    # def movie_repository(self):
    #     return self.movie_repository
    
    # @property
    # def reserve_repository(self):
    #     return self.reserve_repository
    
    
