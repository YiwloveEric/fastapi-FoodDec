from fastapi import APIRouter, Depends
from model.models import History
from dependence.depends import get_user_id_from_token

hisRouter = APIRouter()


@hisRouter.get("/")
async def get_his(user_id: int = Depends(get_user_id_from_token)):
    # 提取用户id的所有his返回
    his = await History.filter(user_id=user_id)
    return his


@hisRouter.delete("/{his_id}")
async def delete_his(his_id: int):
    his = await History.get(history_id=his_id)
    await his.delete()
    return {"msg": "delete ok"}
