# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity_table',
            name='login_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 184736)),
        ),
        migrations.AlterField(
            model_name='activity_table',
            name='logout_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 184736)),
        ),
        migrations.AlterField(
            model_name='admin_table',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 183736)),
        ),
        migrations.AlterField(
            model_name='black_list',
            name='black_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 183736)),
        ),
        migrations.AlterField(
            model_name='login_error_table',
            name='forbid_end_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 184736)),
        ),
        migrations.AlterField(
            model_name='login_error_table',
            name='forbid_start_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 184736)),
        ),
        migrations.AlterField(
            model_name='manage_deal',
            name='deal_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 15, 18, 49, 48, 183736)),
        ),
    ]
