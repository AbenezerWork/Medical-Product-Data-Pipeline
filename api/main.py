from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud
from . import schemas
from .database import get_db

app = FastAPI(title="Kara Solutions Medical Data API")


@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct], tags=["Reports"])
def read_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returns the top N most frequently mentioned medical products or drugs.
    """
    products = crud.get_top_products(db, limit=limit)
    return products


@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity], tags=["Reports"])
def read_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    """
    Returns the daily posting activity for a specific channel.
    """
    activity = crud.get_channel_activity(db, channel_name=channel_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="Channel not found")
    return activity


@app.get("/api/search/messages", response_model=List[schemas.Message], tags=["Search"])
def read_search_messages(query: str, db: Session = Depends(get_db)):
    """
    Searches for messages containing a specific keyword.
    """
    messages = crud.search_messages(db, query=query)
    return messages
