from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy import insert, update, select, delete
from models.user import User
from schemas import CreateUser, UpdateUser
from backend.db import sync_session

router_user = APIRouter(prefix="/user", tags=["user"])


@router_user.get("/")
async def all_users():
    with sync_session() as session:
        users = session.scalars(select(User))
        return users.all()


@router_user.get("/user_id")
async def user_by_id(user_id: int):
    with sync_session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
        return user


@router_user.post("/create")
async def create_user(user: CreateUser):
    with sync_session() as session:
        new_user = session.scalar(select(User).where(User.username == user.username))
        if new_user is None:
            session.add(User(
                               username=user.username,
                               lastname=user.lastname,
                               firstname=user.firstname,
                               age=user.age,
                               slug=slugify(user.username))
            )
            session.commit()
        else:
            return {
                'status_code': status.HTTP_404_NOT_FOUND,
                'transaction': 'The user is already in the database',
            }
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'User created successfully',
        }


@router_user.put("/update")
async def update_user(user: UpdateUser, user_id: int):

    with sync_session() as session:
        user_by = session.scalar(select(User).where(User.id == user_id))
        if user_by is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

        session.execute(update(User).where(User.id == user_id).values(username=user.username,
                                                                 lastname=user.lastname,
                                                                 firstname=user.firstname,
                                                                 age=user.age,
                                                                 slug=slugify(user.username)))
        session.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User updated successfully',
        }


@router_user.delete("/delete")
async def delete_user(user_id: int):
    with sync_session() as session:
        user_by = session.scalar(select(User).where(User.id == user_id))
        if user_by is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
        session.execute(delete(User).where(User.id == user_id))
        session.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User deleted successfully',
        }
