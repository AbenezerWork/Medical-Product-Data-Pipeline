# schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class Message(BaseModel):
    message_id: int
    channel_id: int
    message_text: Optional[str]
    message_views: Optional[int]
    message_datetime: datetime

    class Config:
        orm_mode = True


class TopProduct(BaseModel):
    product: str
    mention_count: int


class ChannelActivity(BaseModel):
    date: date
    post_count: int
