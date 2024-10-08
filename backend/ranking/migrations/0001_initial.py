# Generated by Django 4.2.9 on 2024-08-29 21:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.PositiveIntegerField(verbose_name='주차')),
                ('score', models.FloatField(default=0.0, verbose_name='점수 합산')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 시각')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ranking', to='account.generation', verbose_name='운영 기수')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranking', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '랭킹',
                'verbose_name_plural': '랭킹',
                'db_table': 'ranking',
                'ordering': ['week'],
            },
        ),
    ]
