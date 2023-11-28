from fastapi import APIRouter, Depends
from dependence.depends import get_user_id_from_token
from model.models import Favorites
from pydantic import BaseModel

favRouter = APIRouter()


class FavIn(BaseModel):
    favorites_id: int
    note: str


@favRouter.get("/")
async def get_fav(user_id: int = Depends(get_user_id_from_token)):
    # 根据用户id筛选出该用户的收藏夹信息
    fav = await Favorites.filter(user=user_id)
    return fav


@favRouter.post("/")
async def post_fav():
    # 还没有写
    pass


@favRouter.delete("/{fav_id}")
async def delete_fav(fav_id: int):
    fav = await Favorites.get(favorites_id=fav_id)
    await fav.delete()
    return {"msg": "删除成功"}


@favRouter.put("/{fav_id}")
async def put_fav(favIn: FavIn):
    fav_id = favIn.favorites_id
    note = favIn.note
    await Favorites.filter(favorites_id=fav_id).update(note=note)
    return {"msg": "更新成功"}
