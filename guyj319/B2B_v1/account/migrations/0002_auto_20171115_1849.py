# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitecode_table',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 177735)),
        ),
        migrations.AlterField(
            model_name='invitecode_table',
            name='validity_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 177735)),
        ),
        migrations.AlterField(
            model_name='message_table',
            name='message_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 178735)),
        ),
        migrations.AlterField(
            model_name='record_table',
            name='time_save',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 179735)),
        ),
        migrations.AlterField(
            model_name='record_table',
            name='time_valid',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 179735)),
        ),
        migrations.AlterField(
            model_name='user_info_table',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 180735)),
        ),
        migrations.AlterField(
            model_name='user_info_table',
            name='black_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 180735)),
        ),
    ]
