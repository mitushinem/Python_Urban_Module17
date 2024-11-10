from fastapi import APIRouter, status, HTTPException
from backend.db import sync_session
from slugify import slugify
from sqlalchemy import select, delete, insert, update
from models.task import Task
from models.user import User
from schemas import CreateTask, UpdateTask

router_task = APIRouter(prefix='/task', tags=['task'])


@router_task.get('/')
async def all_tasks():
    with sync_session() as session:
        return session.scalars(select(Task)).all()


@router_task.get('/{task_id}')
async def get_task(task_id: str):
    with sync_session() as session:
        return session.scalars(select(Task).where(Task.id == task_id)).first()


@router_task.post('/create')
async def create_task(task: CreateTask, user_id: int):
    with sync_session() as session:
        user = session.scalar(select(User).where(User.id == user_id))
        if not user:
            return {
                'status_code': status.HTTP_404_NOT_FOUND,
                'transaction': 'User not found',
            }
        session.add(
            Task(
                title=task.title,
                content=task.content,
                slug=slugify(task.title),
                user_id=user.id,
            )
        )
        session.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Task created successfully',
        }


@router_task.put('/update')
async def update_task(task: UpdateTask, id: int):
    with sync_session() as session:
        task_user = session.scalar(select(Task).where(Task.id == id))

        if task_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")

        session.execute(update(Task).where(Task.id == id).values(title=task.title,
                                                                 content=task.content,
                                                                 slug=slugify(task.title),
                                                                 ))
        session.commit()

        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Task update successfully',
        }


@router_task.delete('/delete')
async def delete_task(task_id: int):
    with sync_session() as session:
        task_del = session.scalar(select(Task).where(Task.id == task_id))
        if task_del is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
        session.execute(delete(Task).where(Task.id == task_id))
        session.commit()
        return {
            'status_code': status.HTTP_204_NO_CONTENT,
            'transaction': 'Task deleted successfully',
        }