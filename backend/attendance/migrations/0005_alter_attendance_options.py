# Generated by Django 4.2.9 on 2024-02-28 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_alter_attendance_user_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['-request_time']},
        ),
    ]