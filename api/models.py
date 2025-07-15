# models.py

from sqlalchemy import Column, BigInteger, Integer, String, Boolean, DateTime, Text
from .database import Base


class Message(Base):
    __tablename__ = 'fct_messages'
    __table_args__ = {'schema': 'marts'}

    message_id = Column(BigInteger, primary_key=True, index=True)
    channel_id = Column(BigInteger)
    date_day = Column(DateTime)
    message_text = Column(Text)
    message_length = Column(Integer)
    message_views = Column(Integer)
    has_image = Column(Boolean)
    message_datetime = Column(DateTime)


class Channel(Base):
    __tablename__ = 'dim_channels'
    __table_args__ = {'schema': 'marts'}

    channel_id = Column(BigInteger, primary_key=True, index=True)
    channel_name = Column(String)
