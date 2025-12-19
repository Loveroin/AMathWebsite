from sqlalchemy import (
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Attempt(Base):
    """
    做题记录（Attempt）

    表示：某个用户，对某一道题，进行的一次作答
    """

    __tablename__ = "attempts"

    # =====================================================
    # Primary Key
    # =====================================================
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        comment="做题记录 ID"
    )

    # =====================================================
    # Foreign Keys
    # =====================================================
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="用户 ID"
    )

    problem_id: Mapped[int] = mapped_column(
        ForeignKey("problems.id"),
        nullable=False,
        index=True,
        comment="题目 ID"
    )

    user = relationship(
        "User",
        backref="attempts"
    )

    problem = relationship(
        "Problem",
        backref="attempts"
    )

    # =====================================================
    # Answer & Result
    # =====================================================
    user_answer: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="用户提交的答案"
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment="是否答对"
    )

    # =====================================================
    # Optional Metadata
    # =====================================================
    time_spent: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="做题耗时（秒）"
    )

    # =====================================================
    # Timestamp
    # =====================================================
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="提交时间"
    )

    def __repr__(self) -> str:
        return (
            f"<Attempt id={self.id} "
            f"user_id={self.user_id} "
            f"problem_id={self.problem_id} "
            f"is_correct={self.is_correct}>"
        )
