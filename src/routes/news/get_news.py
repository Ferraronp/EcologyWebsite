import logging
from fastapi import APIRouter, Response
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
    db_sess = db_session.create_session()
    for news in db_sess.query(News).all():
        dict_ = dict()
        dict_['id'] = news.id
        dict_['title'] = news.title
        dict_['content'] = news.content
        dict_['url'] = news.url
        dict_['date'] = news.date
        news_list.append(dict_)
    return news_list


@router.get("/get_news_img")
def get_news(news_id: int):
    db_sess = db_session.create_session()
    news_img = db_sess.query(News).filter(News.id == news_id).first().img
    return Response(news_img)


@router.on_event("startup")
@repeat_every(seconds=60 * 5)
def update_news():
    logging.info('Updating news in database')
    news_list = list()
    news_list.extend(get_news_ecosphere_press())
    news_list.extend(eco_portalsu_parser())
    for i in news_list:
        try:
            db_sess = db_session.create_session()
            news = News()
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
