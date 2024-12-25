from fastapi import APIRouter, HTTPException, Response, Request
from database.db_utils import get_user_by_username, add_user, add_event, get_all_events
from model.user_model import UserCreate, UserResponse, UserLogin
from model.event_model import EventCreate, EventResponse
from utils import verify_password, hash_password, verify_access_token, create_access_token
from typing import List


router = APIRouter()
#limiter = Limiter(key_func=get_remote_address)

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, response: Response):

    # Hash the password and try to add the user to the database
    new_user = add_user(username=user.username, email=user.email, password=hash_password(user.password))

    # If the user already exists, return a 400 error
    if new_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    
    access_token = create_access_token(data={"sub": new_user.email})

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="strict")

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

@router.get("/verify-token")
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

@router.post("/create_event")
async def create_event(event: EventCreate):
    new_event = add_event(event.name, event.location, event.start_time, event.end_time, event.description, event.create_by)
    print("New Event: ", new_event)
    return {"message": "Event created successfully"}

@router.get("/get_events", response_model=List[EventResponse])
async def get_events():
    events = get_all_events()
    
    return [EventResponse(
        name=event[0],  # 第 0 個元素為 name
        location=event[1],  # 第 1 個元素為 location
        start_time=event[2].strftime("%Y-%m-%d %H:%M:%S"),  # 第 2 個元素為 start_time，轉為字串
        end_time=event[3].strftime("%Y-%m-%d %H:%M:%S"),  # 第 3 個元素為 end_time，轉為字串
        description=event[4]  # 第 4 個元素為 description
    ) for event in events]