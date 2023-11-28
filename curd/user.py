from jose import jwt
from model.models import User
from typing import Any, Union
from security.security import ALGORITHM
from fastapi import HTTPException


async def get_user_by_id(user_id: int):
    user = await User.filter(user_id=user_id)
    if user:
        return user
    return None


async def get_user_by_name(username: str):
    user = await User.get(name=username)
    if not user:
        raise HTTPException(status_code=401,detail="用户未注册")
    return user


async def user_register_save(username: str) -> Any:
    # 先到微信接口进行获取信息

    # 获取到了信息之后，进行保存
    user = User(name=username, openid=openid)
    await user.save()
    return 1

async def get_user_his_by_id(id:int):
    pass
