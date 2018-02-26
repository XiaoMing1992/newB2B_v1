# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car_table',
            name='black_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 171735)),
        ),
        migrations.AlterField(
            model_name='car_table',
            name='date_publish',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 171735)),
        ),
        migrations.AlterField(
            model_name='car_table',
            name='date_valid',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 171735)),
        ),
        migrations.AlterField(
            model_name='car_table',
            name='delivery_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 171735)),
        ),
        migrations.AlterField(
            model_name='invalid_time_car_table',
            name='black_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 173735)),
        ),
        migrations.AlterField(
            model_name='invalid_time_car_table',
            name='date_publish',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 173735)),
        ),
        migrations.AlterField(
            model_name='invalid_time_car_table',
            name='date_valid',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 173735)),
        ),
        migrations.AlterField(
            model_name='invalid_time_car_table',
            name='delivery_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 172735)),
        ),
    ]
