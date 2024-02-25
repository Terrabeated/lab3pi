from fastapi import (
    APIRouter, 
    HTTPException, 
    status, 
    Depends)

from ..config.db import get_db

from ..models import Event as EventDbModel

from ..schemas import BaseEvent, Event, EventPreview

from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from typing import List

router = APIRouter(
    prefix="/api/events",
    tags=["API"]
)
  
@router.get("/", response_description="Get All events", response_model=List[EventPreview], status_code=status.HTTP_200_OK)
def get_all_events(db: Session=Depends(get_db)):

    stmt = select(EventDbModel.id, EventDbModel.type, EventDbModel.description)
    events = db.execute(stmt).fetchall()

    if events == []:
        db.rollback()
        raise HTTPException(db, status.HTTP_404_NOT_FOUND, f"Nothing found")
    return events


@router.get("/id/{id}", response_description="Get event by id", response_model=Event, status_code=status.HTTP_200_OK)
def get_event_by_id(id: int, db: Session=Depends(get_db)):

    stmt = select(EventDbModel).where(EventDbModel.id == id).limit(1)
    event = db.execute(stmt).scalar()

    if event is None:
        db.rollback()
        raise HTTPException(db, status.HTTP_404_NOT_FOUND, f"Nothing found")

    return event


@router.post("/", response_description="Create new event", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: BaseEvent, db: Session=Depends(get_db)):

    try:
        new_event = db.execute(
            insert(EventDbModel).returning(EventDbModel), 
            [{**event.model_dump()}]
        ).scalar()

    except:
        db.rollback()
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Error occuring while creating new event")
    else:
        db.commit()
        return new_event
    
@router.get("/type/{type}", response_description="Get events by type", response_model=List[EventPreview], status_code=status.HTTP_200_OK)
def get_events_by_type(type:str, db:Session=Depends(get_db)):

    statement = select(EventDbModel.id, EventDbModel.type, EventDbModel.description).where(EventDbModel.type==type) 
    events = db.execute(statement).fetchall()
    if events==[]:
        db.rollback()
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"there are no events with {type} type")
    else:
        return events

    