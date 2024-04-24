import os

from django.core.management import BaseCommand

from account.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        django_env = os.getenv("DJANGO_ENV", "dev")

        if django_env != "dev":
            if User.objects.count() == 0:
                username = os.getenv("DJANGO_SUPERUSER_USERNAME", "")
                email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
                password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "")

                User.objects.create_superuser(
                    email=email, username=username, password=password, role="관리자", workout_level=0, profile_number=0
                )
