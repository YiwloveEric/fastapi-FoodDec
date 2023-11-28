from fastapi import FastAPI
import uvicorn
from tortoise.contrib.fastapi import register_tortoise
from user.urls import userRouter
from settings import TORTOISE_ORM
from api.AllRouter import allrouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # *：代表所有客户端
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(allrouter)
app.include_router(userRouter)

register_tortoise(
    app,
    config=TORTOISE_ORM,
    # generate_schemas=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
