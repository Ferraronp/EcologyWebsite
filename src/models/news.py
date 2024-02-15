from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    title: str
    date: datetime
    content: str
    img: bytes
    url: str


class NewsList(BaseModel):
    news: list[News]
