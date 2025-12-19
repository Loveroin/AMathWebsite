from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.problem import (
    ProblemCreate,
    ProblemOut,
    ProblemListOut,
    ProblemUpdate,
)
from app.crud import problem as crud_problem
from app.routers.deps import get_current_user, get_current_superuser
from app.models.user import User


router = APIRouter()


# =====================================================
# Public APIs（不需要登录）
# =====================================================

@router.get(
    "",
    response_model=ProblemListOut,
    summary="获取题目列表",
)
def read_problem_list(
    *,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    difficulty: Optional[int] = Query(None, ge=1, le=5),
    problem_type: Optional[str] = Query(None),
):
    """
    题目列表（分页 + 筛选）
    """
    total, items = crud_problem.get_problem_list(
        db=db,
        skip=skip,
        limit=limit,
        difficulty=difficulty,
        problem_type=problem_type,
        is_active=True,
    )

    return {
        "total": total,
        "items": items,
    }


@router.get(
    "/{problem_id}",
    response_model=ProblemOut,
    summary="获取单个题目",
)
def read_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: int,
):
    """
    获取单个题目详情
    """
    problem = crud_problem.get_problem_by_id(
        db=db,
        problem_id=problem_id,
    )

    if not problem or not problem.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )

    return problem


# =====================================================
# Admin APIs（需要管理员）
# =====================================================

@router.post(
    "",
    response_model=ProblemOut,
    status_code=status.HTTP_201_CREATED,
    summary="创建题目（管理员）",
)
def create_problem(
    *,
    db: Session = Depends(get_db),
    problem_in: ProblemCreate,
    current_user: User = Depends(get_current_superuser),
):
    """
    创建题目（仅管理员）
    """
    problem = crud_problem.create_problem(
        db=db,
        problem_in=problem_in,
        created_by_id=current_user.id,
    )

    return problem


@router.patch(
    "/{problem_id}",
    response_model=ProblemOut,
    summary="更新题目（管理员）",
)
def update_problem(
    *,
    db: Session = Depends(get_db),
    problem_id: int,
    problem_in: ProblemUpdate,
    current_user: User = Depends(get_current_superuser),
):
    """
    更新题目（仅管理员）
    """
    problem = crud_problem.get_problem_by_id(
        db=db,
        problem_id=problem_id,
    )

    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )

    problem = crud_problem.update_problem(
        db=db,
        problem=problem,
        problem_in=problem_in,
    )

    return problem
