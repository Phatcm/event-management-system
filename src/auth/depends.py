from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token
from src.db.redis import token_in_blacklist
from src.db.main import get_session
from .service import UserService
from src.db.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Any, List

user_service = UserService()


class CustomTokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        print("Creds scheme: ", creds.scheme)
        print("Creds credential: ", creds.credentials)
        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token"
            )

        if await token_in_blacklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is Invalid or has been Revoked",
                    "Resolution": "Please accquire a new token",
                },
            )

        # if token_data is not None:
        #     if token_data["refresh"]:
        #         raise HTTPException(
        #             status_code=status.HTTP_403_FORBIDDEN,
        #             detail="Please provide an valid Access Token",
        #         )
        # else:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or Expired Token"
        #     )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes")


# To check if a valid access token is provided to an endpoint
class AccessTokenBearer(CustomTokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an valid Access Token",
            )


# To check if a valid refresh token is provided to an endpoint
class RefreshTokenBearer(CustomTokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an valid Refresh Token",
            )


async def get_current_user(
    token_detail: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_detail["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not allowed to perform this.",
        )