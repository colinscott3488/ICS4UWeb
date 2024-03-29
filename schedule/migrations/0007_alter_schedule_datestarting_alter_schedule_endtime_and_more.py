# Generated by Django 4.2.6 on 2023-12-13 21:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_rename_job_number_schedule_jobcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='dateStarting',
            field=models.DateField(default=datetime.datetime(2023, 12, 13, 16, 24, 43, 464845)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='endTime',
            field=models.TimeField(default=datetime.datetime(2023, 12, 13, 16, 24, 43, 464860)),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='jobCode',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='startTime',
            field=models.TimeField(default=datetime.datetime(2023, 12, 13, 16, 24, 43, 464855)),
        ),
    ]
