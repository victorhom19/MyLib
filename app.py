import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from auth.database import get_async_session
from config import FRONTEND_ORIGIN, BACKEND_HOST, BACKEND_PORT
from models.models import User, Role
from routes.auth_router import auth_router, register_router, current_user, reset_password_router, verify_router
from routes.authors_router import authors_router
from routes.books_router import books_router
from routes.collections_router import collections_router


app = FastAPI()

origins = [
    FRONTEND_ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    register_router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    reset_password_router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    verify_router,
    prefix="/auth",
    tags=["auth"],
)



app.include_router(books_router)
app.include_router(authors_router)
app.include_router(collections_router)



if __name__ == '__main__':
    uvicorn.run(app=app, host=f"{BACKEND_HOST}", port=BACKEND_PORT)