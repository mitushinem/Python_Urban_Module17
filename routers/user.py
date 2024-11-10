from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy import insert, update, select, delete
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models.user import User
from schemas import CreateUser, UpdateUser

router_user = APIRouter(prefix="/user", tags=["user"])

@router_user.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users


@router_user.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.execute(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    return user


@router_user.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], user: CreateUser):
    # user_by = db.scalars(select(User).where(User.username == user.username)).all()
    # if user_by is not None:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    db.execute(insert(User).values(username=user.username,
                                   lastname=user.lastname,
                                   firstname=user.firstname,
                                   age=user.age,
                                   slug=slugify(user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User created successfully',
    }


@router_user.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user: UpdateUser, user_id: int):
    user_by = db.execute(select(User).where(User.id == user_id))
    if user_by is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    db.execute(update(User).where(User.id == user_id).values(username=user.username,
                                                             lastname=user.lastname,
                                                             firstname=user.firstname,
                                                             age=user.age,
                                                             slug=slugify(user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User updated successfully',
    }


@router_user.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_by = db.scalar(select(User).where(User.id == user_id))
    if user_by is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted successfully',
    }
