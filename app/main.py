import uvicorn
import fastapi
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.core.models import database as _models
from app.database import engine as _engine


from app.routers import (
    users as users_router,
    notes as notes_router,
    quiz as quiz_router
)

_models.Base.metadata.create_all(bind=_engine)


def get_application():
    app = fastapi.FastAPI(title=settings.PROJECT_NAME)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(users_router.router)
    app.include_router(notes_router.router)
    app.include_router(quiz_router.router)

    return app


app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
