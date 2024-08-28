from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch import receiver

from account.models import Generation
from ranking.models import Ranking
from ranking.services import get_problems_score, get_weeks_in_generation
from record.models import BoulderProblem

@receiver(post_save, sender=BoulderProblem)
def update_ranking_on_post_save(sender: BoulderProblem, instance: BoulderProblem, created: bool, raw: bool, using: str, **kwargs) -> None:
    # add the new score
    generation: Generation = instance.record.generation
    week: int = get_weeks_in_generation(instance.record.start_time.date())
    ranking, _ = Ranking.objects.get_or_create(user=instance.record.user, generation=generation, week=week)
    ranking.score += get_problems_score(instance.record.user.workout_level, instance.workout_level, instance.count)
    ranking.save()

@receiver(pre_save, sender=BoulderProblem)
def update_ranking_on_pre_save(sender: BoulderProblem, instance: BoulderProblem, raw: bool, using: str, update_fields: list, **kwargs) -> None:
    # substract the old score
    try:
        old_instance: BoulderProblem = BoulderProblem.objects.get(pk=instance.pk)
    except BoulderProblem.DoesNotExist:
        return
    generation: Generation = old_instance.record.generation
    week: int = get_weeks_in_generation(old_instance.record.start_time.date())
    ranking: Ranking = Ranking.objects.get(user=old_instance.record.user, generation=generation, week=week)
    ranking.score -= get_problems_score(old_instance.record.user.workout_level, old_instance.workout_level, old_instance.count)
    if ranking.score <= 0:
        ranking.delete()
    else:
        ranking.save()

@receiver(pre_delete, sender=BoulderProblem)
def update_ranking_on_delete(sender: BoulderProblem, instance: BoulderProblem, using: str, **kwargs) -> None:
    generation: Generation = instance.record.generation
    week: int = get_weeks_in_generation(instance.record.start_time.date())
    try:
        ranking: Ranking = Ranking.objects.get(user=instance.record.user, generation=generation, week=week)
    except Ranking.DoesNotExist:
        return
    ranking.score -= get_problems_score(instance.record.user.workout_level, instance.workout_level, instance.count)
    if ranking.score <= 0:
        ranking.delete()
    else:
        ranking.save()