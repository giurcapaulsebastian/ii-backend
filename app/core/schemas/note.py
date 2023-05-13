import datetime as _dt

import pydantic as _pydantic


class _NoteBase(_pydantic.BaseModel):
    title: str
    content: str


class NoteCreate(_NoteBase):
    pass


class Note(_NoteBase):
    created_at: _dt.datetime
    updated_at: _dt.datetime

    class Config:
        orm_mode = True
