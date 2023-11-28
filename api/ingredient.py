from fastapi import APIRouter
from model.models import User, Ingredient

ingreRouter = APIRouter()


@ingreRouter.get("/")
async def get_inge_all():
    ingredient_allQuerySet = await Ingredient.all()
    return ingredient_allQuerySet
