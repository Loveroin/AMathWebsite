from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models.problem import Problem
from app.schemas.problem import ProblemCreate, ProblemUpdate


# =====================================================
# Create
# =====================================================

def create_problem(
    db: Session,
    *,
    problem_in: ProblemCreate,
    created_by_id: Optional[int] = None,
) -> Problem:
    """
    创建题目
    """
    problem = Problem(
        title=problem_in.title,
        content=problem_in.content,
        problem_type=problem_in.problem_type,
        difficulty=problem_in.difficulty,
        options=problem_in.options,
        correct_answer=problem_in.correct_answer,
        created_by_id=created_by_id,
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    return problem


# =====================================================
# Read (Single)
# =====================================================

def get_problem_by_id(
    db: Session,
    *,
    problem_id: int,
) -> Optional[Problem]:
    """
    根据 ID 获取题目
    """
    return db.get(Problem, problem_id)


# =====================================================
# Read (List)
# =====================================================

def get_problem_list(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 20,
    difficulty: Optional[int] = None,
    problem_type: Optional[str] = None,
    is_active: bool = True,
) -> Tuple[int, List[Problem]]:
    """
    获取题目列表（分页 + 筛选）
    返回 (total, items)
    """

    stmt = select(Problem)

    if is_active is not None:
        stmt = stmt.where(Problem.is_active == is_active)

    if difficulty is not None:
        stmt = stmt.where(Problem.difficulty == difficulty)

    if problem_type is not None:
        stmt = stmt.where(Problem.problem_type == problem_type)

    # ✅ 关键点 1：明确 total 一定是 int
    total: int = db.scalar(
        select(func.count()).select_from(stmt.subquery())
    ) or 0

    # ✅ 关键点 2：明确 items 是 List[Problem]
    items: List[Problem] = (
        db.scalars(
            stmt.offset(skip).limit(limit)
        )
        .all()
    )

    return total, items


# =====================================================
# Update
# =====================================================

def update_problem(
    db: Session,
    *,
    problem: Problem,
    problem_in: ProblemUpdate,
) -> Problem:
    """
    更新题目（部分字段）
    """
    update_data = problem_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(problem, field, value)

    db.commit()
    db.refresh(problem)

    return problem


# =====================================================
# Statistics
# =====================================================

def increase_submit_count(
    db: Session,
    *,
    problem_id: int,
    is_correct: bool,
) -> None:
    """
    提交一次答案后更新统计信息
    """
    problem = db.get(Problem, problem_id)
    if not problem:
        return

    problem.submit_count += 1
    if is_correct:
        problem.correct_count += 1

    db.commit()
