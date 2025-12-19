from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.crud.user import (
    get_user_by_username,
    get_user_by_email,
    create_user,
)
from app.schemas.user import UserCreate, UserOut


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


# =====================================================
# 注册
# =====================================================

@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """
    用户注册
    """

    # 1️⃣ 检查用户名是否存在
    if get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # 2️⃣ 检查邮箱是否存在
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 3️⃣ 哈希密码
    hashed_password = get_password_hash(user_in.password)

    # 4️⃣ 创建用户
    user = create_user(
        db,
        user_in=user_in,
        hashed_password=hashed_password,
    )

    return user


# =====================================================
# 登录
# =====================================================

@router.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    """
    用户登录，返回 JWT Access Token
    """

    # 1️⃣ 查用户
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # 2️⃣ 校验密码
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # 3️⃣ 检查用户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    # 4️⃣ 生成 JWT
    access_token = create_access_token(subject=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
