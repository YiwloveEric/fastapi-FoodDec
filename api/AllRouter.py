from fastapi import APIRouter
from api.fav import favRouter
from api.ingredient import ingreRouter
from api.ocr import ocrRouter
from api.his import hisRouter

allrouter = APIRouter(prefix="/api")

allrouter.include_router(favRouter, prefix="/fav", tags=["收藏夹接口"])
allrouter.include_router(ingreRouter, prefix="/ing", tags=["知识库接口"])
allrouter.include_router(ocrRouter, prefix="/ocr", tags=["ocr接口"])
allrouter.include_router(hisRouter, prefix="/his", tags=["历史记录接口"])
