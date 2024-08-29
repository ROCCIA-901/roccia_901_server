from datetime import datetime

from account.models import Generation
from config import exceptions


def get_problems_score(user_level: int, problem_level: int, count: int) -> float:
    """
    사용자의 레벨과 문제의 레벨을 바탕으로 점수를 계산하는 메서드입니다.
    """
    if problem_level < user_level:
        return count * 0.5
    elif problem_level == user_level:
        return count * 1.0
    else:
        return count * 2.0


def get_weeks_in_generation(target_date: datetime.date) -> int:  # type: ignore
    """
    기수의 시작일과 종료일을 바탕으로 몇 주차인지 계산하는 메서드입니다.
    """
    try:
        generation = Generation.objects.get(start_date__lte=target_date, end_date__gte=target_date)
    except Exception:
        raise exceptions.NotExistException("기수 정보가 존재하지 않습니다.")
    delta = target_date - generation.start_date
    week = delta.days // 7 + 1
    return week
