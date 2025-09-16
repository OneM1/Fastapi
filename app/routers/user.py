from typing import List
from fastapi import FastAPI, Depends, HTTPException,APIRouter
from sqlmodel import Session, select
from .. import models,schemes
from .. database import  get_session
from .. import utils


router = APIRouter(prefix="/users",tags=['users'])


@router.post("/",response_model=schemes.UserResponse)
def create_user(user:schemes.CreateUser,session:Session= Depends(get_session)):
    statement = select(models.Users).where(
        (models.Users.email == user.email) |
        (models.Users.username == user.username)
    )
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user = models.Users(**user.model_dump())
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
    if new_user.email == models.Users.email or new_user.name == models.Users.name:
        raise HTTPException(status_code=500,detail="user with email already exists")
    

@router.put("/{user_id}",response_model=schemes.UserResponse)
def UpdateUser(user_id:int,update_user:schemes.UpdateUser,session:Session = Depends(get_session)):
    updated_user = session.get(models.Users,user_id)
    updated_user.email = update_user.email
    updated_user.username = update_user.username
    updated_user.password = update_user.password
    session.commit()
    session.refresh(updated_user)
    return updated_user

@router.delete("/{user_id}",response_model=schemes.UserResponse)
def DeleteUser(user_id:int,session:Session=Depends(get_session)):
    deleted_user = session.get(models.Users,user_id)
    session.delete(deleted_user)
    session.commit()
    return deleted_user

@router.get("/",response_model=List[schemes.UserResponse])
def getUsers(session:Session=Depends(get_session)):
    users=session.exec(select(models.Users)).all()
    return users

@router.get("/{user_id}",response_model=schemes.UserResponse)
def getUsers(user_id:int,session:Session=Depends(get_session)) -> models.Users:
    usersbyid=session.get(models.Users,user_id)
    if not usersbyid:
        raise HTTPException(status_code=404,detail=f'couldnt find user with id {user_id}')
    return usersbyid

