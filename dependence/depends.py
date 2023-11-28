from typing import Optional
from fastapi import Header
from security.security import check_jwt_token


async def get_user_id_from_token(token: Optional[str] = Header(...)) -> int:
    user_id = check_jwt_token(token).get("user_id")
    return user_id
