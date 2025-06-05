from fastapi import APIRouter
from .game import route as gameRoute

route = APIRouter()

route.include_router(gameRoute)