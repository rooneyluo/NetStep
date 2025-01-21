from fastapi import APIRouter, HTTPException
from database.db_utils import add_event, fetch_all_events
from model.event_model import EventCreate, EventResponse
from utils.utils import setup_logger
from typing import List

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/create_event", response_model=EventResponse)
async def create_event(event: EventCreate):
    try:
        new_event = add_event(
            title=event.title,
            description=event.description,
            organizer_id=event.organizer_id,
            location_id=event.location_id,
            start_time=event.start_time,
            end_time=event.end_time,
            created_by=event.created_by,
            updated_by=event.updated_by,
            current_participants=event.current_participants,
            max_participants=event.max_participants,
            status=event.status,
            tags=event.tags,
            likes=event.likes,
            dislikes=event.dislikes
        )
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    if new_event is None:
        logger.warning(f"Failed to create event {event.title}")
        raise HTTPException(status_code=400, detail="Failed to create event")
    
    logger.info(f"Event {new_event.title} created successfully")

    return EventResponse(**new_event)

@router.get("/get_events", response_model=List[EventResponse])
async def get_events():
    try:
        events = fetch_all_events()
    except Exception as e:
        logger.error(f"Error fetching events: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return [EventResponse(**event) for event in events]