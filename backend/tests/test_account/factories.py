import factory

from account.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"username{n}")
    generation = factory.Iterator(["1기", "2기", "3기", "4기", "5기", "6기", "7기", "8기", "9기", "10기", "11기"])
    role = factory.Iterator(["운영진", "부원", "관리자"])
    workout_location = factory.Iterator(
        ["더클라임 일산", "더클라임 연남", "더클라임 양재", "더클라임 신림", "더클라임 마곡"]
    )
    workout_level = factory.Iterator([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    profile_number = factory.Iterator([1, 2, 3, 4, 5, 6, 7, 8])
    introduction = factory.Faker("text", max_nb_chars=500)
    created_at = factory.Faker("past_datetime", start_date="-30d")  # 지난 30일 내의 날짜
    updated_at = factory.Faker("date_time")
    is_active = True
    is_staff = False
