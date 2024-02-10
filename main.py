from fastapi import APIRouter, FastAPI
import logging

from src.routes.news import get_news

logging.basicConfig(filename='logs.log',
                    level=logging.WARNING,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

api_router = APIRouter()
api_router.include_router(get_news.router, prefix="/get_news")

app = FastAPI()
app.include_router(api_router)
