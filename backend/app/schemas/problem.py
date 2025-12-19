from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, Field


# =====================================================
# Base
# =====================================================

class ProblemBase(BaseModel):
    """
    题目公共字段
    """
    title: str = Field(..., description="题目标题")
    content: str = Field(..., description="题目内容（支持 LaTeX）")

    problem_type: str = Field(
        ...,
        description="题目类型：single / multiple / numeric / text"
    )

    difficulty: int = Field(
        ...,
        ge=1,
        le=5,
        description="难度等级（1~5）"
    )

    options: Optional[Dict[str, str]] = Field(
        default=None,
        description="选择题选项（非选择题为 null）"
    )


# =====================================================
# Create
# =====================================================

class ProblemCreate(ProblemBase):
    """
    创建题目（管理员 / 出题人）
    """
    correct_answer: str = Field(
        ...,
        description="正确答案（选择题为 A/B/C，多选为 A,B；填空为字符串）"
    )


# =====================================================
# Update
# =====================================================

class ProblemUpdate(BaseModel):
    """
    更新题目（部分更新）
    """
    title: Optional[str] = None
    content: Optional[str] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    options: Optional[Dict[str, str]] = None
    correct_answer: Optional[str] = None
    is_active: Optional[bool] = None


# =====================================================
# Read / Response
# =====================================================

class ProblemOut(ProblemBase):
    """
    返回给前端的题目结构
    """
    id: int

    submit_count: int
    correct_count: int
    is_active: bool

    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# List Response
# =====================================================

class ProblemListOut(BaseModel):
    """
    题目列表响应（分页用）
    """
    total: int
    items: List[ProblemOut]
