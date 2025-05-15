from src.modules.auth.interfaces.token_repository import TokenRepository
# from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
from src.modules.user.interfaces.user_repository import UserRepository
# from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
# from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
# from src.modules.reserve.infrastructure.postgres_reserve_repository import PostgresReserveRepository
from src.modules.auth.interfaces.password_hasher_repository import PasswordHasher
# from src.modules.auth.infrastructure.bycrypt_password_hasher import BcryptPasswordHasher



class Provider:
    def __init__(
            self,
            db_session,
            user_repository,
            token_repository,
            password_hasher_repository,
            movie_repository,
            reserve_repository
            ):

        self.db_session = db_session
        self.user_repository= user_repository
        self.token_repository= token_repository
        self.password_hasher_repository= password_hasher_repository
        self.movie_repository= movie_repository
        self.reserve_repository= reserve_repository
        
