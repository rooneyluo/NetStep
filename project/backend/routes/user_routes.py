import logging
from fastapi import APIRouter, HTTPException, Response, Request
from database.db_utils import get_user_by_username, add_user, add_event, get_all_events
from model.user_model import UserCreate, UserResponse, UserLogin
from model.event_model import EventCreate, EventResponse
from utils import verify_password, hash_password, verify_access_token, create_access_token
from typing import List

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, response: Response):
    # Hash the password and try to add the user to the database
    try:
        new_user = add_user(username=user.username, email=user.email, password=hash_password(user.password))
    except Exception as e:
        logger.error(f"Error adding user to the database: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    # If the user already exists, return a 400 error
    if new_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    
    access_token = create_access_token(data={"sub": new_user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")

    logger.info(f"User {new_user.username} registered successfully")

    return UserResponse(username=new_user.username, email=new_user.email)

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin, response: Response):
    # Fetch user from the database by email
    db_user = get_user_by_username(user.email)
    
    # Check if user exists and verify the password
    if db_user is None or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")

    return UserResponse(username=db_user.username, email=db_user.email)

@router.get("/verify-token", response_model=UserResponse)
async def verify_token(request: Request):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=403, detail="Not authenticated")

    user_email = verify_access_token(token)

    if user_email == "Token expired":
        raise HTTPException(status_code=403, detail="Token expired. Please log in again.")
    
    if user_email == "Invalid token":
        raise HTTPException(status_code=403, detail="Invalid token. Please log in again.")

    user = get_user_by_username(user_email)

    if user is None:
        raise HTTPException(status_code=403, detail="User not found. Please log in again.")
    
    # Token is valid, return success message
    return UserResponse(username=user.username, email=user.email)

@router.post("/logout")
async def logout(response: Response):
    # Set the access_token cookie to an empty value and expire it
    response.set_cookie(key="access_token", value="", httponly=True, max_age=0, expires=0)
    return {"message": "Successfully logged out"}


@router.post("/create_event", response_model=EventResponse)
async def create_event(event: EventCreate):
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
    logger.info(f"Event {new_event.title} created successfully")
    return EventResponse(
        title=new_event.title,
        description=new_event.description,
        organizer_id=new_event.organizer_id,
        location_id=new_event.location_id,
        start_time=new_event.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        end_time=new_event.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        created_by=new_event.created_by,
        current_participants=new_event.current_participants,
        max_participants=new_event.max_participants,
        status=new_event.status,
        tags=new_event.tags,
        likes=new_event.likes,
        dislikes=new_event.dislikes
    )

@router.get("/get_events", response_model=List[EventResponse])
async def get_events():
    events = get_all_events()
    return [EventResponse(
        title=event[0],
        description=event[1],
        organizer_id=event[2],
        location_id=event[3],
        start_time=event[4].strftime("%Y-%m-%d %H:%M:%S"),
        end_time=event[5].strftime("%Y-%m-%d %H:%M:%S"),
        created_by=event[6],
        current_participants=event[7],
        max_participants=event[8],
        status=event[9],
        tags=event[10],
        likes=event[11],
        dislikes=event[12]
    ) for event in events]