from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    organizer_id: str
    location_id: str
    start_time: datetime
    end_time: datetime
    created_by: str
    updated_by: Optional[str] = None
    current_participants: int = Field(0, ge=0)
    max_participants: int = Field(..., ge=1)
    status: str = Field(..., pattern="^(active|cancelled|completed|expired)$")
    tags: Optional[str] = None
    likes: int = Field(0, ge=0)
    dislikes: int = Field(0, ge=0)

class EventResponse(BaseModel):
    title: str
    description: str
    organizer_id: str
    location_id: str
    start_time: str
    end_time: str
    created_by: str
    current_participants: int
    max_participants: int
    status: str
    tags: Optional[str] = None
    likes: int
    dislikes: int