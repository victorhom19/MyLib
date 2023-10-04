from fastapi import HTTPException, status, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import auth_backend
from auth.database import get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from cache.cache import get_cache_instance
from models.models import User, Role

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)

register_router = fastapi_users.get_register_router(UserRead, UserCreate)

reset_password_router = fastapi_users.get_reset_password_router()

verify_router = fastapi_users.get_verify_router(UserRead)

current_user = fastapi_users.current_user()


@auth_router.get("/status")
async def auth_status(user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session)):
    role = await session.get(Role, user.role_id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": {
            "value": role.role.value,
            "name": role.role.name
        }
    }


@verify_router.post("/exchange_code")
@reset_password_router.post("/exchange_code")
async def exchange_code(code: str):
    cache = get_cache_instance()
    token = cache.get(code)
    if token is None:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT)
    cache.delete(code)
    return {"token": token}



