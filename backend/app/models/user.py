from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class User(Base):
    """
    用户表（User）

    只描述「数据库结构」，不写任何业务逻辑：
    - 不校验密码
    - 不生成 JWT
    - 不判断权限
    """

    __tablename__ = "users"

    # ===== 主键 =====
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        comment="用户唯一 ID"
    )

    # ===== 基础信息 =====
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        comment="用户名（唯一）"
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        comment="邮箱（唯一，用于登录/找回密码）"
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="密码哈希值（绝不存明文）"
    )

    # ===== 状态字段 =====
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="是否激活（封号用）"
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="是否管理员"
    )

    # ===== 时间戳 =====
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="创建时间"
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="更新时间"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username}>"
