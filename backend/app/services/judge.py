from app.models.problem import Problem


# =====================================================
# Public API
# =====================================================

def judge_answer(
    *,
    problem: Problem,
    user_answer: str,
) -> bool:
    """
    判题主入口
    """
    problem_type = problem.problem_type

    if problem_type == "single_choice":
        return _judge_single_choice(problem, user_answer)

    if problem_type == "multiple_choice":
        return _judge_multiple_choice(problem, user_answer)

    if problem_type == "numeric":
        return _judge_numeric(problem, user_answer)

    if problem_type == "text":
        return _judge_text(problem, user_answer)

    raise ValueError(f"Unsupported problem type: {problem_type}")


# =====================================================
# Judge Implementations
# =====================================================

def _judge_single_choice(problem: Problem, user_answer: str) -> bool:
    correct = problem.correct_answer.strip().upper()
    user = user_answer.strip().upper()
    return user == correct


def _judge_multiple_choice(problem: Problem, user_answer: str) -> bool:
    correct_set = {
        x.strip().upper()
        for x in problem.correct_answer.split(",")
        if x.strip()
    }
    user_set = {
        x.strip().upper()
        for x in user_answer.split(",")
        if x.strip()
    }
    return user_set == correct_set


def _judge_numeric(problem: Problem, user_answer: str) -> bool:
    try:
        correct = float(problem.correct_answer)
        user = float(user_answer)
    except ValueError:
        return False

    EPSILON = 1e-6
    return abs(user - correct) <= EPSILON


def _judge_text(problem: Problem, user_answer: str) -> bool:
    return user_answer.strip() == problem.correct_answer.strip()
