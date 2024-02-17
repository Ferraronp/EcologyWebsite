from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    id: int
    title: str
    date: datetime
    content: str
    url: str
