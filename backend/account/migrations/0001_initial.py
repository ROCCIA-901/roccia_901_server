# Generated by Django 4.2.9 on 2024-08-29 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='기수')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='시작 날짜')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='종료 날짜')),
            ],
            options={
                'verbose_name': '기수',
                'verbose_name_plural': '기수',
                'db_table': 'generation',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=320, unique=True, verbose_name='이메일')),
                ('username', models.CharField(max_length=20, verbose_name='사용자 이름')),
                ('role', models.CharField(choices=[('운영진', '운영진'), ('부원', '부원'), ('관리자', '관리자')], default='부원', max_length=10, verbose_name='역할')),
                ('workout_location', models.CharField(choices=[('더클라임 일산', '더클라임 일산'), ('더클라임 연남', '더클라임 연남'), ('더클라임 양재', '더클라임 양재'), ('더클라임 신림', '더클라임 신림'), ('더클라임 마곡', '더클라임 마곡'), ('더클라임 홍대', '더클라임 홍대'), ('더클라임 서울대', '더클라임 서울대'), ('더클라임 강남', '더클라임 강남'), ('더클라임 사당', '더클라임 사당'), ('더클라임 신사', '더클라임 신사'), ('더클라임 논현', '더클라임 논현'), ('더클라임 문래', '더클라임 문래')], max_length=100, verbose_name='지점')),
                ('workout_level', models.IntegerField(choices=[(1, '하얀색'), (2, '노란색'), (3, '주황색'), (4, '초록색'), (5, '파란색'), (6, '빨간색'), (7, '보라색'), (8, '회색'), (9, '갈색'), (10, '검정색')], verbose_name='난이도')),
                ('profile_number', models.IntegerField(verbose_name='프로필 번호')),
                ('introduction', models.TextField(max_length=500, verbose_name='소개글')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성 일시')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정 일시')),
                ('is_active', models.BooleanField(default=False, verbose_name='활성 여부')),
                ('is_staff', models.BooleanField(default=False, verbose_name='스태프 여부')),
                ('generation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to='account.generation', verbose_name='가입 기수')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '부원',
                'verbose_name_plural': '부원',
                'db_table': 'user',
            },
        ),
    ]
