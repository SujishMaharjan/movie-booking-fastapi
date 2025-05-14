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

    is_admin(user)
    reserves = ListAllReservesService(provider).execute()
    return [AllReserveResponse(**vars(reserve)) for reserve in reserves]

@router.get("/me")
async def get_self_reserve_resource(
    request: Request,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    reserve = GetUserReserveOwn(provider).execute(user)
    return ReserveUserResponse(**vars(reserve))


@router.post("/")
async def create_reserve_resource(
    request: Request,
    model:models.AddReserveModel,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    is_member(user)
    try:
        reserve = MovieReserveService(provider).execute(model,user)
        provider.db_session.commit()
    except Exception as e:
        provider.db_session.rollback()
        #logger.debug("Failed to reserve movies")
        raise FailedToSaveException(f"Failed to Reserve: {str(e)}") from e

    return ReserveResponse(**reserve)



@router.post("/unreserve")
async def unreserve_reserve_resource(
    request: Request,
    model:models.UnReserveModel,
    provider: AnnotatedRepositoryProvider,
    user: AnnotatedCurrentUser
):
    is_member(user)
    try:
        unreserve = MovieUnreserveService(provider).execute(model,user)
        provider.db_session.commit()
    except Exception as e:
        provider.db_session.rollback()
        #logger.debug("Failed to reserve movies")
        raise FailedToSaveException(f"Failed to UnReserve: {str(e)}") from e

    return ReserveResponse(**unreserve)


