from fastapi import APIRouter, FastAPI
import logging
from src.routes.news import get_news
from src.routes.auth import aunt, reg

logging.basicConfig(filename='logs.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

api_router = APIRouter(prefix='/api')
api_router.include_router(get_news.router, prefix="/news")
api_router.include_router(aunt.router, prefix="/auth")
api_router.include_router(reg.router, prefix="/reg")
app = FastAPI()
app.include_router(api_router)
