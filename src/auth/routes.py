from fastapi import APIRouter, Depends, status
from .schemas import User, UserCreateModel, UserLoginModel
from .service import UserService
from .utils import create_access_token, decode_token, verify_password
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .depends import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blacklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])
REFRESH_TOKEN_EXPIRY_DAYS = 2


@auth_router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with the email is already exist!",
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
async def login_user(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        valid = verify_password(password, user.password_hash)
        if valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": user.uid,
                    "role": user.role,
                }  # provide expiry too if needed, else will use the default 3600s
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": user.uid,
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
            )
            return JSONResponse(
                content={
                    "message": "Login Sucessfully!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"uid": str(user.uid), "email": user.email},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password."
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_detail: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_detail["exp"]

    if (
        datetime.fromtimestamp(expiry_timestamp) > datetime.now()
    ):  # check the time of the access token
        new_access_token = create_access_token(
            user_data=token_detail["user"],
        )  # create new token from the data
        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired Token."
    )


@auth_router.get("/me")
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(RoleChecker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_detail: dict = Depends(AccessTokenBearer())):
    jti = token_detail["jti"]

    await add_jti_to_blacklist(jti)

    return JSONResponse(
        content={"message": "Logout Successful!"},
        status_code=status.HTTP_200_OK,
    )


# @auth_router.patch("/admin/update_user_role")
# async def update_user_role()
