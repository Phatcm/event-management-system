from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from typing import List
from .service import RSVPService
from src.db.main import get_session
from src.auth.depends import AccessTokenBearer, RoleChecker
from src.db.models import RSVP

rsvp_router = APIRouter()
rsvp_service = RSVPService()
access_token_bearer = AccessTokenBearer()
# role_checker = Depends(RoleChecker(["user"]))


@rsvp_router.get(
    "/",
    response_model=List[RSVP],
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
async def get_rsvps_by_user(
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    user_uid = token_detail.get("user")["user_uid"]
    rsvps = await rsvp_service.get_rsvps_of_user(user_uid, session)
    return rsvps


@rsvp_router.post(
    "/{event_uid}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
async def rsvp_to_event(
    event_uid: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    user_uid = token_detail.get("user")["user_uid"]
    try:
        rsvp_result = await rsvp_service.rsvp_event(event_uid, user_uid, session)
        return rsvp_result  # Return the RSVP result if successful
    except ValueError as e:
        # If the error is raised by the service, return it as an HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400 for bad request
            detail=str(e),  # Pass the error message from the exception
        )


@rsvp_router.delete(
    "/{rsvp_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RoleChecker(["admin", "user"]))],
)
async def cancel_rsvp(
    rsvp_uid: str,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(access_token_bearer),
):
    user_uid = token_detail.get("user")["user_uid"]
    try:
        cancel_result = await rsvp_service.cancel_rsvp(rsvp_uid, session)
        return cancel_result
    except ValueError as e:
        # If the error is raised by the service, return it as an HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400 for bad request
            detail=str(e),  # Pass the error message from the exception
        )
