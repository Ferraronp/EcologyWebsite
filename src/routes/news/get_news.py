import logging
from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every

from src.routes.news.parsers.ecosphere_press_parser import get_news_ecosphere_press
from src.routes.news.parsers.eco_portal_parser import eco_portalsu_parser

from src.routes.news.database.models.news_model import News
from .database import db_session


db_session.global_init("src/routes/news/database/news.db")
router = APIRouter()


@router.get("/get_news")
def get_news():
    news_list = list()
    try:
        for news in get_news_ecosphere_press():
            news_list.append(News(**news))
    except Exception as ex:
        logging.error(f"Can't parse ecosphere.press {ex}")
    return news_list


@router.on_event("startup")
@repeat_every(seconds=60 * 5)
def update_news():
    db_sess = db_session.create_session()
    news_list = list()
    news_list.extend(get_news_ecosphere_press())
    news_list.extend(eco_portalsu_parser())
    for i in news_list:
        try:
            news = News()
            news.title = i['title']
            news.date = i['date']
            news.content = i['content']
            news.img = i['img']
            news.url = i['url']
            db_sess.add(news)
        except Exception:
            pass
    db_sess.commit()
