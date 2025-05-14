from fastapi import APIRouter, Request,Depends
from src.entrypoints.api.reserve import models
from src.modules.reserve.application.reserve_movie import MovieReserveService
from src.modules.reserve.application.get_self_reserve_details import GetUserReserveOwn
from src.modules.reserve.application.unreserve_movies import MovieUnreserveService
from src.modules.reserve.application.get_all_reserves import ListAllReservesService
from src.entrypoints.api.reserve.responses import ReserveResponse, ReserveUserResponse,AllReserveResponse
from src.core.dependencies import AnnotatedRepositoryProvider,AnnotatedCurrentUser
from src.core.security import is_admin,is_member
from src.core.exceptions import FailedToSaveException
from src.core.log_config import logger


router = APIRouter(
    prefix="/reserves",
    tags=["Reserves"]
)

@router.get("/")
async def get_reserve_resource(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    logger.info("User %s requested info for user %s", user.id)
    is_admin(user)
    reserves = ListAllReservesService(provider).execute()
    logger.debug("Retrieved data %d reserves", len(reserves))
    return [AllReserveResponse(**vars(reserve)) for reserve in reserves]

@router.get("/me")
async def get_self_reserve_resource(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    logger.info("User %s requested reservation info",user.username)
    reserves = GetUserReserveOwn(provider).execute(user)
    logger.debug("Reserve data retrieved for user %s", user.id)
    return [ReserveUserResponse(**vars(reserve)) for reserve in reserves]


@router.post("/")
async def create_reserve_resource(
    request: Request,
    model:models.AddReserveModel,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    
    is_member(user)
    logger.info("User %s requested reservation for movie %s", user.id,model.movie_id)
    reserve = MovieReserveService(provider).execute(model,user)
    return ReserveResponse(**reserve)



@router.post("/unreserve")
async def unreserve_reserve_resource(
    request: Request,
    model:models.UnReserveModel,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    is_member(user)
    logger.info("User: %s requested unreservation for reservation_id: %s", user.id,model.reserve_id)
    unreserve = MovieUnreserveService(provider).execute(model,user)
    return ReserveResponse(**unreserve)


