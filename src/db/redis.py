import redis.asyncio as redis
from src.config import Config

JTI_EXPIRY = 3600

# URL-based connection
token_blacklist = redis.from_url(Config.REDIS_URL, decode_responses=True)


# Add JTI to blacklist with expiration time
async def add_jti_to_blacklist(jti: str) -> None:
    await token_blacklist.set(name=jti, value="", ex=JTI_EXPIRY)


# Check if JTI is in blacklist
async def token_in_blacklist(jti: str) -> bool:
    jti_value = await token_blacklist.get(jti)
    return jti_value is not None
