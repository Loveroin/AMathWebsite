from sqlalchemy import (
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Problem(Base):
    """
    题目表（Problem）

    表示系统中的一道题目
    """

    __tablename__ = "problems"

    # =====================================================
    # Primary Key
    # =====================================================
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        comment="题目 ID"
    )

    # =====================================================
    # Basic Info
    # =====================================================
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="题目标题"
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="题目内容（支持 LaTeX）"
    )

    problem_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="题目类型：single / multiple / numeric / text"
    )

    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="难度等级（1~5）"
    )

    # =====================================================
    # Choice Options
    # =====================================================
    options: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
        comment="选择题选项（非选择题为 null）"
    )

    # =====================================================
    # Answer (NEVER expose to frontend)
    # =====================================================
    correct_answer: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="正确答案"
    )

    # =====================================================
    # Statistics
    # =====================================================
    submit_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="提交次数"
    )

    correct_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="答对次数"
    )

    # =====================================================
    # Status
    # =====================================================
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="是否启用"
    )

    # =====================================================
    # Ownership
    # =====================================================
    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        comment="出题人（管理员）ID"
    )

    created_by = relationship(
        "User",
        backref="created_problems"
    )

    # =====================================================
    # Timestamp
    # =====================================================
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="创建时间"
    )

    def __repr__(self) -> str:
        return (
            f"<Problem id={self.id} "
            f"type={self.problem_type} "
            f"difficulty={self.difficulty}>"
        )
