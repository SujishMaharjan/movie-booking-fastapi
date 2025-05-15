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
        
