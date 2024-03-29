# Generated by Django 4.2.6 on 2023-12-11 15:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_rename_field2_schedule_apple_schedule_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='apple',
            new_name='jobCode',
        ),
        migrations.AddField(
            model_name='schedule',
            name='endTime',
            field=models.TimeField(default=datetime.datetime(2023, 12, 11, 15, 37, 51, 141616)),
        ),
        migrations.AddField(
            model_name='schedule',
            name='startTime',
            field=models.TimeField(default=datetime.datetime(2023, 12, 11, 15, 37, 51, 141605)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
