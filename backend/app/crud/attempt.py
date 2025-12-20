from typing import List, Tuple
from sqlalchemy import func


from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.attempt import Attempt
from app.models.problem import Problem
from app.services.judge import judge_answer
from app.schemas.attempt import AttemptCreate


# =====================================================
# Create
# =====================================================

def create_attempt(
    db: Session,
    *,
    user_id: int,
    attempt_in: AttemptCreate,
) -> Attempt:
    """
    创建一次做题记录（提交答案）
    """

    # 1️⃣ 获取题目
    problem = db.get(Problem, attempt_in.problem_id)
    if not problem:
        raise ValueError("Problem not found")

    # 2️⃣ 判题
    is_correct = judge_answer(
        problem=problem,
        user_answer=attempt_in.user_answer,
    )

    # 3️⃣ 创建 Attempt
    attempt = Attempt(
        user_id=user_id,
        problem_id=problem.id,
        user_answer=attempt_in.user_answer,
        is_correct=is_correct,
        time_spent=attempt_in.time_spent,
    )

    db.add(attempt)

    # 4️⃣ 更新题目统计
    problem.submit_count += 1
    if is_correct:
        problem.correct_count += 1

    db.commit()
    db.refresh(attempt)

    return attempt


# =====================================================
# Read
# =====================================================

def get_attempt_list_by_user(
    db: Session,
    *,
    user_id: int,
    skip: int = 0,
    limit: int = 20,
) -> Tuple[int, List[Attempt]]:
    """
    获取某个用户的做题记录列表
    返回 (total, items)
    """

    stmt = (
        select(Attempt)
        .where(Attempt.user_id == user_id)
        .order_by(Attempt.created_at.desc())
    )

    # ✅ total 明确是 int
    total: int = db.scalar(
        select(func.count()).select_from(stmt.subquery())
    ) or 0

    # ✅ 显式转换为 list，类型检查通过
    items = list(
        db.scalars(
            stmt.offset(skip).limit(limit)
        )
    )

    return total, items
