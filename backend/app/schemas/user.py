from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# =====================================================
# 基础 Schema（公共字段）
# =====================================================

class UserBase(BaseModel):
    """
    用户公共字段（不会直接作为请求或响应）
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="用户名"
    )
    email: EmailStr = Field(
        ...,
        description="用户邮箱"
    )


# =====================================================
# 创建用户（注册时用）
# =====================================================

class UserCreate(UserBase):
    """
    用户注册请求体
    """
    password: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="明文密码（只在注册/登录时出现）"
    )


# =====================================================
# 更新用户（可选，后期用）
# =====================================================

class UserUpdate(BaseModel):
    """
    用户信息更新（支持部分更新）
    """
    username: str | None = Field(
        None,
        min_length=3,
        max_length=50
    )
    email: EmailStr | None = None
    password: str | None = Field(
        None,
        min_length=6,
        max_length=128
    )


# =====================================================
# 数据库 -> API 响应
# =====================================================

class UserOut(UserBase):
    """
    返回给前端的用户信息
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True  # 支持 SQLAlchemy ORM 对象


# =====================================================
# 简化版用户（嵌套使用）
# =====================================================

class UserPublic(BaseModel):
    """
    用于题目、记录等场景的简化用户信息
    """
    id: int
    username: str

    class Config:
        from_attributes = True
