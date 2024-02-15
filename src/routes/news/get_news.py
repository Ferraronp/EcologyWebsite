import logging
from fastapi import APIRouter

from ...models.news import News, NewsList
from src.routes.news.support_files.ecosphere_press_parser import get_news_ecosphere_press


router = APIRouter()


@router.get("/get_news", response_model=NewsList)
def get_news():
    news_list = list()
    try:
        for news in get_news_ecosphere_press():
            news_list.append(News(**news))
    except Exception as ex:
        logging.error(f"Can't parse ecosphere.press {ex}")
    return NewsList(news=news_list)
