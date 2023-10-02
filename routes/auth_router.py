from fastapi import HTTPException, status
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from cache.cache import get_cache_instance
from models.models import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)

register_router = fastapi_users.get_register_router(UserRead, UserCreate)

reset_password_router = fastapi_users.get_reset_password_router()

verify_router = fastapi_users.get_verify_router(UserRead)


@verify_router.post("/exchange_code")
@reset_password_router.post("/exchange_code")
async def exchange_code(code: str):
    cache = get_cache_instance()
    token = cache.get(code)
    if token is None:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    cache.delete(code)
    return {"token": token}


current_user = fastapi_users.current_user()
