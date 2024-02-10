import datetime
import logging

from fastapi import APIRouter
from ...models.news import News


router = APIRouter()


@router.get("/", response_model=News)
def get_news():
    try:
        pass
    except Exception as ex:
        logging.error(f"Can't parse ecoportal.su {ex}")
    return News(title='test', date=datetime.datetime.now(), content='test2', img='test3'.encode())
