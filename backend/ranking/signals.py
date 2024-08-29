from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from account.models import Generation
from ranking.models import Ranking
from ranking.services import get_problems_score, get_weeks_in_generation
from record.models import BoulderProblem


@receiver(post_save, sender=BoulderProblem)
def update_ranking_on_post_save(
    sender: BoulderProblem, instance: BoulderProblem, created: bool, raw: bool, using: str, **kwargs
) -> None:
    """
    BoulderProblem 모델의 인스턴스가 생성되거나 업데이트될 때 호출되는 함수입니다.
    인스턴스의 workout_level과 count를 기반으로 계산된 score가 Ranking 모델에 합산됩니다.
    인스턴스에 연결된 Record 모델의 generation과 week에 Ranking 인스턴스가 존재하지 않으면, 새로 생성됩니다.
    """
    generation: Generation = instance.record.generation
    try:
        week: int = get_weeks_in_generation(instance.record.start_time.date())
    except Exception:
        return
    ranking, _ = Ranking.objects.get_or_create(user=instance.record.user, generation=generation, week=week)
    ranking.score += get_problems_score(instance.record.user.workout_level, instance.workout_level, instance.count)
    ranking.save()


@receiver(pre_save, sender=BoulderProblem)
def update_ranking_on_pre_save(
    sender: BoulderProblem, instance: BoulderProblem, raw: bool, using: str, update_fields: list, **kwargs
) -> None:
    """
    BoulderProblem 모델의 인스턴스가 업데이트되기 전에 호출되는 함수입니다.
    인스턴스의 workout_level과 count를 기반으로 계산된 score가 Ranking 모델에 감산됩니다.
    Ranking 인스턴스의 score가 0 이하일 경우 삭제됩니다.
    """
    try:
        old_instance: BoulderProblem = BoulderProblem.objects.get(pk=instance.pk)
    except BoulderProblem.DoesNotExist:
        return
    generation: Generation = old_instance.record.generation
    try:
        week: int = get_weeks_in_generation(old_instance.record.start_time.date())
    except Exception:
        return
    ranking: Ranking = Ranking.objects.get(user=old_instance.record.user, generation=generation, week=week)
    ranking.score -= get_problems_score(
        old_instance.record.user.workout_level, old_instance.workout_level, old_instance.count
    )
    if ranking.score <= 0:
        ranking.delete()
    else:
        ranking.save()


@receiver(pre_delete, sender=BoulderProblem)
def update_ranking_on_delete(sender: BoulderProblem, instance: BoulderProblem, using: str, **kwargs) -> None:
    """
    BoulderProblem 모델의 인스턴스가 삭제되기 전에 호출되는 함수입니다.
    인스턴스의 workout_level과 count를 기반으로 계산된 score가 Ranking 모델에 감산됩니다.
    Ranking 인스턴스의 score가 0 이하일 경우 삭제됩니다.
    """
    generation: Generation = instance.record.generation
    try:
        week: int = get_weeks_in_generation(instance.record.start_time.date())
    except Exception:
        return
    try:
        ranking: Ranking = Ranking.objects.get(user=instance.record.user, generation=generation, week=week)
    except Ranking.DoesNotExist:
        return
    ranking.score -= get_problems_score(instance.record.user.workout_level, instance.workout_level, instance.count)
    if ranking.score <= 0:
        ranking.delete()
    else:
        ranking.save()
