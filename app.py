
import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import FRONTEND_ORIGIN, BACKEND_HOST, BACKEND_PORT
from routes.auth_router import auth_router, register_router, reset_password_router, verify_router
from routes.authors_router import authors_router
from routes.books_router import books_router
from routes.collections_router import collections_router
from routes.genres_router import genres_router
from routes.reviews_router import reviews_router

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

app.include_router(
    books_router,
    prefix="/books",
    tags=["books"]
)

app.include_router(
    authors_router,
    prefix="/authors",
    tags=["authors"]
)

app.include_router(
    genres_router,
    prefix="/genres",
    tags=["genres"]
)

app.include_router(
    collections_router,
    prefix="/collections",
    tags=["collections"]
)

app.include_router(
    reviews_router,
    prefix="/reviews",
    tags=["reviews"]
)


if __name__ == '__main__':
    uvicorn.run(app=app, host=f"{BACKEND_HOST}", port=BACKEND_PORT)