# Generated by Django 4.2.9 on 2024-05-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_delete_passwordupdateemailauthstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, help_text='활성 상태'),
        ),
    ]
