from datetime import datetime

from account.models import Generation
from config.exceptions import NotExistException


def get_problems_score(user_level: int, problem_level: int, count: int) -> float:
    if problem_level < user_level:
        return count * 0.5
    elif problem_level == user_level:
        return count * 1.0
    else:
        return count * 2.0

def get_weeks_in_generation(target_date: datetime.date) -> int:
   try:
        generation = Generation.objects.get(start_date__lte=target_date, end_date__gte=target_date)
   except Exception:
       raise Exception("기수 정보가 존재하지 않습니다.")
   delta = target_date - generation.start_date
   week = delta.days // 7 + 1
   return week
