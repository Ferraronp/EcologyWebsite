import logging
from fastapi import APIRouter, Response
from fastapi_utils.tasks import repeat_every

from src.routes.news.parsers.ecosphere_press_parser import get_news_ecosphere_press
from src.routes.news.parsers.eco_portal_parser import eco_portalsu_parser

from src.models.news import News

from src.routes.news.database.models.news_model import News as NewsFromDB
from .database import db_session


db_session.global_init("src/routes/news/database/news.db")
router = APIRouter()


@router.get("/get_news", response_model=list[News])
def get_news():
    news_list = list()
    db_sess = db_session.create_session()
    for news_from_db in db_sess.query(NewsFromDB).all():
        news = News(**news_from_db.__dict__)
        news.id = news_from_db.id
        news.title = news_from_db.title
        news.content = news_from_db.content
        news.url = news_from_db.url
        news.date = news_from_db.date
        news_list.append(news)
    return news_list


@router.get("/get_news_img")
def get_news(news_id: int):
    db_sess = db_session.create_session()
    news_img = db_sess.query(NewsFromDB).filter(NewsFromDB.id == news_id).first().img
    return Response(news_img)


@router.on_event("startup")
@repeat_every(seconds=60 * 5)
def update_news():
    logging.info('Updating news in database')
    news_list = list()
    # news_list.extend(get_news_ecosphere_press())
    # news_list.extend(eco_portalsu_parser())
    for i in news_list:
        try:
            db_sess = db_session.create_session()
            news = NewsFromDB()
            news.title = i['title']
            news.date = i['date']
            news.content = i['content']
            news.img = i['img']
            news.url = i['url']
            db_sess.add(news)
            db_sess.commit()
        except Exception:
            pass
    logging.info('Updated news in database')
