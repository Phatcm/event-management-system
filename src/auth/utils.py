from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt, uuid
import logging

from src.config import Config

password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    hash = password_context.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)


def create_random_secret(length: int = 8) -> str:
    import secrets

    return secrets.token_hex(length)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    # Convert any UUIDs in user_data to strings
    user_data = {
        key: (str(value) if isinstance(value, uuid.UUID) else value)
        for key, value in user_data.items()
    }

    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )  # if not provide expiry time use default
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    token = jwt.encode(
        payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=Config.JWT_ALGORITHM
        )
        return token_data
    except jwt.PyJWTError as error:
        logging.exception(error)
        return None
