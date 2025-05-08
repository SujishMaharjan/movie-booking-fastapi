import uuid
from src.modules.user.interfaces.user_repository import UserRepository
from src.modules.auth.interfaces.token_repository import TokenRepository
from src.modules.movie.interfaces.movie_repository import MovieRepository
from src.modules.user.exceptions import UserNotFoundException,InvalidMemberTypeException
from src.modules.user.entity.user import User,UserRole
from src.modules.movie.entity.movie import Movie
from src.modules.reserve.entity.reserve import Reserve
from src.modules.movie.exceptions import MovieNotFoundException,InvalidSeatsEnteredException
from src.entrypoints.api.reserve.models import AddReserveModel
from src.modules.reserve.interfaces.reserve_repository import ReserveRepository
from datetime import datetime
from src.modules.reserve.exceptions import FailedToSaveException

class MovieReserveService:
    def __init__(self,token:str,user_repo:UserRepository,token_repo:TokenRepository,movie_repo:MovieRepository,reserve_repo:ReserveRepository):
        self.token=token
        self.user_repo=user_repo
        self.token_repo=token_repo
        self.movie_repo=movie_repo
        self.reserve_repo=reserve_repo

    def execute(self,reserve_model:AddReserveModel):
        username = self.token_repo.validate_and_decode_token(self.token)
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UserNotFoundException("User Not Found")
        
        user:User = self.user_repo.to_dataclass(user,User)
        self.is_member(user.role)
        movie:Movie = self.validate_movie_and_seat_to_reserve(reserve_model.movie_id,reserve_model.no_of_seats)
        updated_movie=self.update_movie_before_reserve(movie,reserve_model.no_of_seats)
        updated_reserve,before_reserve_seats=self.create_or_update_reserve(user.id,movie.id,reserve_model.no_of_seats)
        return {
            "username":user.username,
            "movie_name":movie.movie_name,
            "before_reserve_seats":before_reserve_seats,
            **updated_reserve.__dict__
        }
        
        


    def is_member(self,role)->bool:
        if role!=UserRole.MEMBER:
            raise InvalidMemberTypeException("Access denied. Member only.")
        return True
    

    def validate_movie_and_seat_to_reserve(self,movie_id,no_of_seats) -> bool:
    
        movie = self.movie_repo.get_by_id(movie_id)
        if not movie:
            raise MovieNotFoundException("No Such Movie Available")
        
        movie = self.movie_repo.to_dataclass(movie,Movie)
        
        if no_of_seats > movie.available_seats or no_of_seats == 0 :
            raise InvalidSeatsEnteredException("Please Enter Valid Seats")
        return movie
    

    def get_user_existing_reservation(self,user_id,movie_id):
        reserve = self.reserve_repo.get_by_user_id_and_movie_id(user_id,movie_id)
        return reserve
    

    def update_movie_before_reserve(self,movie:Movie,no_of_seats:int):
        update_reserve_seats = movie.reserve_seats +no_of_seats
        update_available_seats =movie.available_seats -no_of_seats
        movie_status = "Fully Reserved" if update_available_seats==0 else movie.movie_status
        try:
            self.movie_repo.update_movie_seats_and_status(
                movie_id=movie.id,
                reserve_seats=update_reserve_seats,
                available_seats=update_available_seats,
                movie_status=movie_status
                )
        except Exception:
            raise FailedToSaveException("Failed to update movie seats and status")
        
        return movie
    

    def create_or_update_reserve(self,user_id:str,movie_id:str,no_of_seats:int):
        try:
            reserve:Reserve = self.get_user_existing_reservation(user_id,movie_id)
            before_reserve_seats = 0
            if not reserve:
                reserve = Reserve(
                    id = str(uuid.uuid4()),
                    user_id = user_id,
                    movie_id = movie_id,
                    user_reserve_seats=no_of_seats,
                    created_at = datetime.now()
                )
                reserve_data = self.reserve_repo.to_persistence_model(reserve)
                self.reserve_repo.save(reserve_data)
            else:
                before_reserve_seats=reserve.user_reserve_seats
                reserve.user_reserve_seats+=no_of_seats
                reserve.updated_at=datetime.now()
                self.reserve_repo.update_reserve_seat(reserve.reserve_id,reserve.user_reserve_seats,reserve.created_at)
        except Exception:
            raise FailedToSaveException("Failed to reserve or update seats")
        return reserve,before_reserve_seats


    
        



    
