from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from fastapi import Header, HTTPException

# 导入配置文件


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
        user_id: Union[int, Any], username: str, expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "user_id": user_id, "name": username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def check_jwt_token(
        token: Optional[str] = Header(...)
) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 当然也可以用 Header(..., alias="Authentication") 或者 alias="X-token"
    :param token:
    :return:
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except (jwt.JWTError, jwt.ExpiredSignatureError, AttributeError):
        # 抛出自定义异常， 然后捕获统一响应
        raise HTTPException(status_code=101, detail="access token fail")
