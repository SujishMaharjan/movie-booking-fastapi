from fastapi import APIRouter, Request,Depends
from src.entrypoints.api.reserve import models
from typing import Annotated
from src.core.infrastucture.persistence.database_postgres import get_db_session
from sqlalchemy.orm import Session
from src.core.dependencies import oauth2_scheme,AnnotatedJwtSettings,AnnotatedHallSettings
from src.modules.auth.infrastructure.Jwt_token_repository import JwtService
from src.modules.user.infrastructure.user_postgres_repository import PostgresUserRepository
from src.modules.movie.infrastructure.movie_postgres_repository import PostgresMovieRepository
from src.modules.reserve.infrastructure.postgres_reserve_repository import PostgresReserveRepository
from src.modules.reserve.application.reserve_movie import MovieReserveService
from src.modules.reserve.application.get_self_reserve_details import GetUserReserveOwn
from src.modules.reserve.application.unreserve_movies import MovieUnreserveService
from src.modules.reserve.application.get_all_reserves import ListAllReservesService
from src.entrypoints.api.reserve.responses import ReserveResponse, ReserveUserResponse,AllReserveResponse


router = APIRouter(
    prefix="/reserves",
    tags=["Reserves"]
)

@router.get("/")
async def get_reserve_resource(
request: Request,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    user_repo = PostgresUserRepository(db_session)
    token_repo = JwtService(jwt_settings)
    reserve_repo = PostgresReserveRepository(db_session)
    reserves = ListAllReservesService(token,user_repo,token_repo,reserve_repo).execute()
    return [AllReserveResponse(**reserve.__dict__) for reserve in reserves]

@router.get("/me")
async def get_self_reserve_resource(
    request: Request,
    jwt_settings: AnnotatedJwtSettings,
    token: Annotated[str,Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    user_repo = PostgresUserRepository(db_session)
    token_repo = JwtService(jwt_settings)
    reserve_repo = PostgresReserveRepository(db_session)
    reserve = GetUserReserveOwn(token,user_repo,token_repo,reserve_repo).execute()
    return ReserveUserResponse(**reserve.__dict__)


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



@router.post("/unreserve")
async def unreserve_reserve_resource(
    request: Request,
    model:models.UnReserveModel,
    token: Annotated[str, Depends(oauth2_scheme)],
    jwt_settings: AnnotatedJwtSettings,
    db_session:Annotated[Session, Depends(get_db_session)]
):
    token_repo=JwtService(jwt_settings)
    user_repo=PostgresUserRepository(db_session)
    movie_repo=PostgresMovieRepository(db_session)
    reserve_repo=PostgresReserveRepository(db_session)
    try:
        unreserve = MovieUnreserveService(token,user_repo,token_repo,movie_repo,reserve_repo).execute(model)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        #logger.debug("Failed to reserve movies")
        raise FailedToSaveException(f"Failed to UnReserve: {str(e)}") from e

    return ReserveResponse(**unreserve)


