from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
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
from app.schemas.token import Token  # 你需要新增这个 schema（下面给你）


router = APIRouter()


# =====================================================
# 注册
# =====================================================
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="注册",
)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    """
    用户注册

    - username/email 唯一
    - password 会被哈希后入库
    """

    # 1) 检查用户名是否存在
    if get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # 2) 检查邮箱是否存在
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 3) 哈希密码
    hashed_password = get_password_hash(user_in.password)

    # 4) 创建用户
    user = create_user(
        db,
        user_in=user_in,
        hashed_password=hashed_password,
    )

    return user


# =====================================================
# 登录（OAuth2 标准）
# =====================================================
@router.post(
    "/login",
    response_model=Token,
    summary="登录（获取 JWT）",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    用户登录，返回 JWT Access Token

    说明：
    - 按 OAuth2 标准，使用 form 表单字段：username / password
    - Swagger 的 Authorize 按钮也会更顺
    """

    # 1) 查用户
    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # 2) 校验密码
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # 3) 检查用户状态
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    # 4) 生成 JWT（subject=用户 id）
    access_token = create_access_token(subject=user.id)

    return {"access_token": access_token, "token_type": "bearer"}
