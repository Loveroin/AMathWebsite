from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


# =====================================================
# Base
# =====================================================

class AttemptBase(BaseModel):
    """
    做题记录公共字段
    """
    problem_id: int = Field(..., description="题目 ID")
    user_answer: str = Field(..., description="用户提交的答案")
    time_spent: Optional[int] = Field(
        None,
        description="做题耗时（秒）"
    )


# =====================================================
# Create (Submit Answer)
# =====================================================

class AttemptCreate(AttemptBase):
    """
    提交答案
    """
    pass


# =====================================================
# Read / Response
# =====================================================

class AttemptOut(BaseModel):
    """
    返回给前端的做题记录
    """
    id: int
    problem_id: int
    user_answer: str
    is_correct: bool

    time_spent: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Submit Result（立即反馈）
# =====================================================

class AttemptResult(BaseModel):
    """
    提交答案后的即时反馈
    """
    is_correct: bool = Field(..., description="是否答对")
    correct_answer: Optional[str] = Field(
        None,
        description="正确答案（仅在需要时返回）"
    )


# =====================================================
# List Response
# =====================================================

class AttemptListOut(BaseModel):
    """
    做题记录列表
    """
    total: int
    items: List[AttemptOut]
