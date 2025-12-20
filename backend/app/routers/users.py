from fastapi import APIRouter, Depends

from app.schemas.user import UserOut
from app.models.user import User
from app.routers.deps import get_current_user


router = APIRouter()


@router.get(
    "/me",
    response_model=UserOut,
)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前登录用户信息

    需要：
        Authorization: Bearer <access_token>
    """
    return current_user
