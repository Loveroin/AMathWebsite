from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.routers.deps import get_current_user
from app.models.user import User
from app.schemas.attempt import (
    AttemptCreate,
    AttemptOut,
    AttemptListOut,
)
from app.crud.attempt import (
    create_attempt,
    get_attempt_list_by_user,
)

router = APIRouter()


# =====================================================
# Submit Answer
# =====================================================

@router.post(
    "",
    response_model=AttemptOut,
    status_code=status.HTTP_201_CREATED,
    summary="提交答案"
)
def submit_attempt(
    attempt_in: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    提交一道题的答案
    """

    try:
        attempt = create_attempt(
            db=db,
            user_id=current_user.id,
            attempt_in=attempt_in,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    return attempt


# =====================================================
# My Attempts
# =====================================================

@router.get(
    "/me",
    response_model=AttemptListOut,
    summary="获取我的做题记录"
)
def read_my_attempts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户的做题记录（分页）
    """

    total, items = get_attempt_list_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )

    return {
        "total": total,
        "items": items,
    }
