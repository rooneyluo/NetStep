from fastapi import APIRouter, HTTPException, Response, Request
from database.db_utils import get_user_by_username_or_email, add_user, add_event, get_all_events
from model.user_model import UserCreate, UserResponse, UserLogin
from model.event_model import EventCreate, EventResponse
from utils import verify_password, hash_password, verify_access_token, create_access_token, setup_logger
from typing import List

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, response: Response):
    # Hash the password and try to add the user to the database
    try:
        new_user = add_user(username=user.username, email=user.email, password=hash_password(user.password))
    except Exception as e:
        logger.error(f"Error adding user to the database: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

    # If the user already exists, return a 400 error
    if new_user is None:
        logger.warning(f"User {user.username} already exists")
        raise HTTPException(status_code=400, detail="User already exists")
    
    access_token = create_access_token(data={"sub": new_user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")

    logger.info(f"User {new_user.username} registered successfully")

    return UserResponse(username=new_user.username, email=new_user.email)

@router.post("/login", response_model=UserResponse)
async def login(user: UserLogin, response: Response):
    # Fetch user from the database by email
    db_user = get_user_by_username_or_email(user.email)
    
    # Check if user exists and verify the password
    if db_user is None or not verify_password(user.password, db_user.password):
        logger.warning(f"Failed login attempt for user {user.email}")
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")

    logger.info(f"User {db_user.username} logged in successfully")

    return UserResponse(username=db_user.username, email=db_user.email)

@router.get("/verify-token", response_model=UserResponse)
async def verify_token(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_username_or_email(payload.get("sub"))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return UserResponse(username=user.username, email=user.email)

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    logger.info("User logged out successfully")
    return {"message": "Logged out successfully"}

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
        events = get_all_events()
    except Exception as e:
        logger.error(f"Error fetching events: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    return [EventResponse(**event) for event in events]