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
            name='UnavailableDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='휴일')),
            ],
            options={
                'verbose_name': '휴일',
                'verbose_name_plural': '휴일',
                'db_table': 'unavailable_dates',
            },
        ),
        migrations.CreateModel(
            name='WeeklyStaffInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('월요일', '월요일'), ('화요일', '화요일'), ('수요일', '수요일'), ('목요일', '목요일'), ('금요일', '금요일')], max_length=10, verbose_name='요일')),
                ('workout_location', models.CharField(blank=True, choices=[('더클라임 일산', '더클라임 일산'), ('더클라임 연남', '더클라임 연남'), ('더클라임 양재', '더클라임 양재'), ('더클라임 신림', '더클라임 신림'), ('더클라임 마곡', '더클라임 마곡'), ('더클라임 홍대', '더클라임 홍대'), ('더클라임 서울대', '더클라임 서울대'), ('더클라임 강남', '더클라임 강남'), ('더클라임 사당', '더클라임 사당'), ('더클라임 신사', '더클라임 신사'), ('더클라임 논현', '더클라임 논현'), ('더클라임 문래', '더클라임 문래')], max_length=100, null=True, verbose_name='지점')),
                ('start_time', models.TimeField(verbose_name='운동 시작 시간')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weekly_staff_info', to='account.generation', verbose_name='기수')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='운영진')),
            ],
            options={
                'verbose_name': '주간 운영진 정보',
                'verbose_name_plural': '주간 운영진 정보',
                'db_table': 'weekly_staff_info',
            },
        ),
        migrations.CreateModel(
            name='AttendanceStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance', models.IntegerField(default=0, verbose_name='출석 횟수')),
                ('late', models.IntegerField(default=0, verbose_name='지각 횟수')),
                ('absence', models.IntegerField(default=0, verbose_name='결석 횟수')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance_stats', to='account.generation', verbose_name='운영 기수')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_stats', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '출석 통계',
                'verbose_name_plural': '출석 통계',
                'db_table': 'attendance_stats',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_location', models.CharField(blank=True, choices=[('더클라임 일산', '더클라임 일산'), ('더클라임 연남', '더클라임 연남'), ('더클라임 양재', '더클라임 양재'), ('더클라임 신림', '더클라임 신림'), ('더클라임 마곡', '더클라임 마곡'), ('더클라임 홍대', '더클라임 홍대'), ('더클라임 서울대', '더클라임 서울대'), ('더클라임 강남', '더클라임 강남'), ('더클라임 사당', '더클라임 사당'), ('더클라임 신사', '더클라임 신사'), ('더클라임 논현', '더클라임 논현'), ('더클라임 문래', '더클라임 문래')], max_length=100, null=True, verbose_name='지점')),
                ('week', models.IntegerField(blank=True, null=True, verbose_name='주차')),
                ('request_time', models.DateTimeField(blank=True, null=True, verbose_name='출석 요청 시간')),
                ('request_processed_status', models.CharField(blank=True, choices=[('승인', '승인'), ('거절', '거절'), ('대기', '대기')], default='대기', max_length=20, null=True, verbose_name='처리 상태')),
                ('request_processed_time', models.DateTimeField(blank=True, null=True, verbose_name='처리 시간')),
                ('attendance_status', models.CharField(blank=True, choices=[('출석', '출석'), ('지각', '지각'), ('결석', '결석'), ('휴일', '휴일')], max_length=20, null=True, verbose_name='출석 상태')),
                ('is_alternate', models.BooleanField(default=False, verbose_name='대체 출석 여부')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attendance', to='account.generation', verbose_name='운영 기수')),
                ('request_processed_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='processed_requests', to=settings.AUTH_USER_MODEL, verbose_name='처리한 사용자')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL, verbose_name='사용자')),
            ],
            options={
                'verbose_name': '출석',
                'verbose_name_plural': '출석',
                'db_table': 'attendance',
                'ordering': ['-request_time'],
            },
        ),
    ]
