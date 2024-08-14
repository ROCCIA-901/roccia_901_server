# Generated by Django 4.2.9 on 2024-08-14 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation', models.CharField(choices=[('1기', '1기'), ('2기', '2기'), ('3기', '3기'), ('4기', '4기'), ('5기', '5기'), ('6기', '6기'), ('7기', '7기'), ('8기', '8기'), ('9기', '9기'), ('10기', '10기'), ('11기', '11기'), ('12기', '12기')], help_text='기수', max_length=10)),
                ('start_date', models.DateField(help_text='기수 시작 날짜')),
                ('end_date', models.DateField(help_text='기수 종료 날짜')),
            ],
            options={
                'db_table': 'activity_dates',
            },
        ),
        migrations.CreateModel(
            name='UnavailableDates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='휴일')),
            ],
            options={
                'db_table': 'unavailable_dates',
            },
        ),
        migrations.CreateModel(
            name='WeeklyStaffInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation', models.CharField(choices=[('1기', '1기'), ('2기', '2기'), ('3기', '3기'), ('4기', '4기'), ('5기', '5기'), ('6기', '6기'), ('7기', '7기'), ('8기', '8기'), ('9기', '9기'), ('10기', '10기'), ('11기', '11기'), ('12기', '12기')], help_text='기수')),
                ('day_of_week', models.CharField(choices=[('월요일', '월요일'), ('화요일', '화요일'), ('수요일', '수요일'), ('목요일', '목요일'), ('금요일', '금요일')], help_text='요일')),
                ('workout_location', models.CharField(choices=[('더클라임 일산', '더클라임 일산'), ('더클라임 연남', '더클라임 연남'), ('더클라임 양재', '더클라임 양재'), ('더클라임 신림', '더클라임 신림'), ('더클라임 마곡', '더클라임 마곡'), ('더클라임 홍대', '더클라임 홍대'), ('더클라임 서울대', '더클라임 서울대'), ('더클라임 강남', '더클라임 강남'), ('더클라임 사당', '더클라임 사당'), ('더클라임 신사', '더클라임 신사'), ('더클라임 논현', '더클라임 논현')], help_text='운동 지점', max_length=100, null=True)),
                ('start_time', models.TimeField(help_text='운동 시작 시간')),
                ('staff', models.ForeignKey(help_text='운영진', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'weekly_staff_info',
            },
        ),
        migrations.CreateModel(
            name='AttendanceStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation', models.CharField(choices=[('1기', '1기'), ('2기', '2기'), ('3기', '3기'), ('4기', '4기'), ('5기', '5기'), ('6기', '6기'), ('7기', '7기'), ('8기', '8기'), ('9기', '9기'), ('10기', '10기'), ('11기', '11기'), ('12기', '12기')], help_text='기수')),
                ('attendance', models.IntegerField(default=0, help_text='출석 횟수')),
                ('late', models.IntegerField(default=0, help_text='지각 횟수')),
                ('absence', models.IntegerField(default=0, help_text='결석 횟수')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_stats', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'attendance_stats',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation', models.CharField(choices=[('1기', '1기'), ('2기', '2기'), ('3기', '3기'), ('4기', '4기'), ('5기', '5기'), ('6기', '6기'), ('7기', '7기'), ('8기', '8기'), ('9기', '9기'), ('10기', '10기'), ('11기', '11기'), ('12기', '12기')], help_text='기수')),
                ('workout_location', models.CharField(choices=[('더클라임 일산', '더클라임 일산'), ('더클라임 연남', '더클라임 연남'), ('더클라임 양재', '더클라임 양재'), ('더클라임 신림', '더클라임 신림'), ('더클라임 마곡', '더클라임 마곡'), ('더클라임 홍대', '더클라임 홍대'), ('더클라임 서울대', '더클라임 서울대'), ('더클라임 강남', '더클라임 강남'), ('더클라임 사당', '더클라임 사당'), ('더클라임 신사', '더클라임 신사'), ('더클라임 논현', '더클라임 논현')], help_text='운동 지점', max_length=100, null=True)),
                ('week', models.IntegerField(help_text='주차', null=True)),
                ('request_time', models.DateTimeField(help_text='출석 요청 시간', null=True)),
                ('request_processed_status', models.CharField(choices=[('승인', '승인'), ('거절', '거절'), ('대기', '대기')], default='대기', help_text='요청 상태', max_length=20, null=True)),
                ('request_processed_time', models.DateTimeField(help_text='요청 처리 시간', null=True)),
                ('attendance_status', models.CharField(choices=[('출석', '출석'), ('지각', '지각'), ('결석', '결석'), ('휴일', '휴일')], help_text='출석 상태', max_length=20, null=True)),
                ('is_alternate', models.BooleanField(default=False, help_text='대체 출석 여부')),
                ('request_processed_user', models.ForeignKey(help_text='요청을 처리한 사용자', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='processed_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'attendance',
                'ordering': ['-request_time'],
            },
        ),
    ]
