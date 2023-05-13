from typing import List

import pydantic as _pydantic


class QuizCreate(_pydantic.BaseModel):
    question: str
    answers: List[str]
    correct_answer: int


class Quiz(_pydantic.BaseModel):
    id: int
    question: str
    answers: List[str]
    correct_answer: int

    class Config:
        orm_mode = True


class QuizResultCreate(_pydantic.BaseModel):
    quiz_id: int
    score: int


class QuizResult(_pydantic.BaseModel):
    id: int
    user_id: int
    score: int

    class Config:
        orm_mode = True
