from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from .documents import User, ToDos
from .models import UserOut, ToDo
from .services.auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from backend.todo import settings
from typing import List


router = APIRouter(prefix="")


@router.post("/register/", status_code=201, response_model=UserOut)
async def register_user(user_data: User):
    user_data.password = get_password_hash(user_data.password)
    return await user_data.save()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


@router.get("/me", response_model=UserOut)
async def get_user_data(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/create/todo")
async def create_todo(todo_data: ToDos, current_user: User = Depends(get_current_user)):
    todo_data.created_by = str(current_user.id)
    return await todo_data.save()


@router.get("/get/todos", response_model=List[ToDo])
async def get_todos():
    return await ToDos.find_all().to_list()
