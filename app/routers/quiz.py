from typing import List

import fastapi
from sqlalchemy import orm

from app.core.schemas import (
    user as _user_schema,
    quiz as _quiz_schema
)
from app.core.services import (
    database as _database_service,
    user as _user_service,
    quiz as _quiz_service
)

router = fastapi.APIRouter()


@router.post("/send_quiz_result", tags=["quizzes"], response_model=_quiz_schema.QuizResult)
async def create_quiz_result(
        quiz_result: _quiz_schema.QuizResultCreate,
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _quiz_service.create_quiz_result(user=user, db=db, quiz=quiz_result)


@router.get("/get_quiz/{quiz_id}", tags=["quizzes"], response_model=_quiz_schema.Quiz)
async def get_quiz(
        quiz_id: int,
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _quiz_service.get_quiz(user=user, db=db, quiz_id=quiz_id)

@router.get("/get_all_quizez", tags=["quizzes"], response_model=List[_quiz_schema.Quiz])
async def get_all_quizes(
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _quiz_service.get_all_quizes(db=db)

@router.get("/quiz_result", tags=["quizzes"], response_model=_quiz_schema.QuizResult)
async def get_quiz_result(
        quiz_id: int,
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _quiz_service.get_quiz_result(user=user, db=db, quiz_id=quiz_id)


@router.get("/quizzes_results", tags=["quizzes"], response_model=List[_quiz_schema.QuizResult])
async def get_quiz_results(
        user: _user_schema.User = fastapi.Depends(_user_service.get_current_user),
        db: orm.Session = fastapi.Depends(_database_service.get_db)
):
    return await _quiz_service.get_quiz_results(user=user, db=db)

