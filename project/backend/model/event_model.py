from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    location: str
    start_time: str
    end_time: str
    description: str
    create_by: str
    """
    image_url: str
    max_participants: int
    min_participants: int
    is_active: bool
    is_full: bool
    is_paid: bool
    is_approved: bool
    is_deleted: bool
    is_cancelled: bool
    is_completed: bool
    is_volunteering: bool
    is_volunteer_open: bool
    """

class EventResponse(BaseModel):
    name: str
    location: str
    start_time: str
    end_time: str
    description: str
