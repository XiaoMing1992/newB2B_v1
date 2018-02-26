# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='activity_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(db_index=True, default=0)),
                ('login_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 709995))),
                ('IP', models.GenericIPAddressField(default='xxx')),
                ('logout_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 709995))),
                ('activity_time', models.CharField(default='xx(h)xx(m)xx(s) ', max_length=50)),
                ('login_state', models.IntegerField(default=0)),
                ('logout_state', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-login_time'],
            },
        ),
        migrations.CreateModel(
            name='inviteCode_error_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('IP', models.GenericIPAddressField(db_index=True, default='xxx')),
                ('error_times', models.IntegerField(default=0)),
                ('forbid_start_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 710995))),
                ('forbid_end_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 710995))),
            ],
        ),
        migrations.CreateModel(
            name='login_error_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('IP', models.GenericIPAddressField(db_index=True, default='xxx')),
                ('error_times', models.IntegerField(default=0)),
                ('forbid_start_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 709995))),
                ('forbid_end_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 709995))),
            ],
        ),
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_name', models.CharField(default='xxx', max_length=100)),
                ('phone', models.CharField(db_index=True, max_length=15)),
                ('password', models.CharField(max_length=500)),
                ('email', models.EmailField(default='xxxx@xx.com', max_length=254)),
                ('reg_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 708995))),
                ('IP', models.GenericIPAddressField(default='xxx')),
                ('is_vip', models.IntegerField(default=0)),
                ('is_black', models.IntegerField(default=0)),
                ('black_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 708995))),
            ],
        ),
    ]
