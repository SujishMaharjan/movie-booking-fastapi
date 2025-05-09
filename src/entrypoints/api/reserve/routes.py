from fastapi import APIRouter, Request,Depends
from src.entrypoints.api.reserve import models
from typing import Annotated
from src.modules.reserve.handlers import *
from src.core.infrastucture.persistence.database_postgres import get_db_session
from sqlalchemy.orm import Session
from src.core.dependencies import oauth2_scheme,AnnotatedJwtSettings,AnnotatedHallSettings
from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.reserve.infrastructure.postgres_reserve_repository import PostgresReserveRepository
from src.modules.reserve.application.reserve_movie import MovieReserveService

router = APIRouter(
    prefix="/reserves",
    tags=["Reserves"]
)

# @router.get("/")
# async def get_reserve_resource(
#     request: Request,
#     db_session:Annotated[Session, Depends(get_db_session)],
#     current_user:Annotated[Users, Depends(get_current_user)]):

#     logger.info("Reserve endpoint accessed")
#     check_user_member_type(current_user,"admin")
#     reserves = list_out_all_reserves(db_session)
#     return reserves

# @router.get("/me")



@router.post("/")
async def create_reserve_resource(
    request: Request,
    model:models.AddReserveModel,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_settings: AnnotatedJwtSettings,
    db_session:Annotated[Session, Depends(get_db_session)]
):
    token_repo=JwtService(jwt_settings)
    user_repo=PostgresUserRepository(db_session)
    movie_repo=PostgresMovieRepository(db_session)
    reserve_repo=PostgresReserveRepository(db_session)
    try:
        reserve = MovieReserveService(token,user_repo,token_repo,movie_repo,reserve_repo).execute(model)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        #logger.debug("Failed to reserve movies")
        raise FailedToSaveException(f"Failed to Reserve: {str(e)}") from e

    return ReserveResponse(**reserve)



# @router.post("/unreserve")
# async def unreserve_reserve_resource(
#     request: Request,
#     model:models.UnReserveModel,
#     db_session:Annotated[Session, Depends(get_db_session)],
#     current_user:Annotated[Users, Depends(get_current_user)]):
    
#     # breakpoint()
#     check_user_member_type(current_user,"member")
#     reserve,movie= check_valid_movie_entered(db_session,current_user,model.movie_name)
#     check_valid_seats_entered_to_unreserve(reserve,model.no_of_seats)
#     reserve_response =  persist_unreserve_to_db(db_session,movie,model.no_of_seats,reserve,current_user)
#     return reserve_response



