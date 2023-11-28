from fastapi import APIRouter, HTTPException, Header
from tortoise.exceptions import DoesNotExist
from curd.user import get_user_by_name
from typing import Optional
from pydantic import BaseModel

from security.security import create_access_token, check_jwt_token

userRouter = APIRouter(prefix="/user", tags=["用户模块"])


class UserIn(BaseModel):
    username: str


@userRouter.post("/login")
async def login(user_in: UserIn):
    try:
        username = user_in.username
        user = await get_user_by_name(username)
        user_id = user.user_id
        token = create_access_token(user_id, username)
        return {"msg": "ok", "token": token}
    except DoesNotExist as e:
        return {"error": str(e)}


@userRouter.get("/test", description="这个使用来进行测试的")
async def jwt_token(token: Optional[str] = Header(...)):
    user = check_jwt_token(token)
    print(user.get("user_id"))
    print(user.get("name"))
    return user

# @userRouter.post("/register")
# def register(username: str):
#     # 根据用户上传的用户名，检查是否已经有用户
#     usered = get_user_by_name(username)
#     if usered:
#         raise HTTPException(status_code=400, detail="用户已存在,请更改你的姓名")
#     # 到微信接口进行过去openid
#
#     # 保存用户注册信息
#
#     # 生成用户注册的token
#     token = create_access_token(user_id, username)
#     return {"token": token}
