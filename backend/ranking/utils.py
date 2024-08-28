def get_problems_score(user_level: int, problem_level: int, count: int) -> float:
    if problem_level < user_level:
        return count * 0.5
    elif problem_level == user_level:
        return count * 1.0
    else:
        return count * 2.0