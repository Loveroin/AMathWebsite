from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.user import User
from app.schemas.user import UserCreate


# =====================================================
# 查询用户
# =====================================================

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    通过 ID 获取用户
    """
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_username(db: Session, username: str) -> User | None:
    """
    通过用户名获取用户
    """
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    通过邮箱获取用户
    """
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


# =====================================================
# 创建用户
# =====================================================

def create_user(
    db: Session,
    *,
    user_in: UserCreate,
    hashed_password: str
) -> User:
    """
    创建新用户

    注意：
    - hashed_password 必须在外部生成
    - crud 不负责密码加密
    """

    user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# =====================================================
# 更新用户
# =====================================================

def update_user(
    db: Session,
    *,
    user: User,
    **kwargs
) -> User:
    """
    更新用户字段（部分更新）

    用法：
        update_user(db, user, username="new", email="xxx")
    """

    for field, value in kwargs.items():
        if value is not None and hasattr(user, field):
            setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user
