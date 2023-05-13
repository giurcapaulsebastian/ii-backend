import fastapi
from sqlalchemy import orm as _orm

from app.core.models import database as _models
from app.core.schemas import user as _user_schema
from app.core.schemas import quiz as _quiz_schema


async def _quiz_selector(user: _user_schema.User, db: _orm.Session, quiz_id: int):
    quiz = db.query(_models.Quiz).filter(_models.Quiz.id == quiz_id).first()
    return quiz


async def _quiz_results_selector(user: _user_schema.User, db: _orm.Session, quiz_id: int):
    quiz = db.query(_models.QuizResults).filter(_models.QuizResults.user_id == user.id, _models.QuizResults.quiz_id == quiz_id).first()
    return quiz


async def create_quiz_result(user: _user_schema.User, db: _orm.Session, quiz: _quiz_schema.QuizResultCreate):
    quiz = _models.QuizResults(**quiz.dict())
    quiz.user_id = user.id
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return _quiz_schema.QuizResult.from_orm(quiz)


async def get_quiz(user: _user_schema.User, db: _orm.Session, quiz_id: int):
    quiz = await _quiz_selector(db=db, quiz_id=quiz_id, user=user)
    if quiz is None:
        raise fastapi.HTTPException(status_code=404, detail="Quiz with this id doesn't exist!")
    return _quiz_schema.Quiz.from_orm(quiz)


async def get_quiz_result(user: _user_schema.User, db: _orm.Session, quiz_id: int):
    quiz = await _quiz_results_selector(db=db, quiz_id=quiz_id, user=user)
    if quiz is None:
        raise fastapi.HTTPException(status_code=404, detail="User doesn't have a quiz result for this quiz")
    return _quiz_schema.QuizResult.from_orm(quiz)


async def get_quiz_results(user: _user_schema.User, db: _orm.Session):
    quizzes = db.query(_models.QuizResults).filter(_models.QuizResults.user_id == user.id).all()
    if quizzes is None:
        raise fastapi.HTTPException(status_code=404, detail="User doesn't have quizs")
    return list(map(_quiz_schema.QuizResult.from_orm, quizzes))
