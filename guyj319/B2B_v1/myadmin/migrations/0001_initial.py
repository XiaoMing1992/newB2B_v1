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
                ('admin_id', models.IntegerField(db_index=True, default=0)),
                ('login_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 706995))),
                ('IP', models.GenericIPAddressField(default='xxx')),
                ('logout_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 707995))),
                ('activity_time', models.CharField(default='xx(h)xx(m)xx(s) ', max_length=50)),
                ('login_state', models.IntegerField(default=0)),
                ('logout_state', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-login_time'],
            },
        ),
        migrations.CreateModel(
            name='admin_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(default='admin', max_length=200)),
                ('username', models.CharField(db_index=True, max_length=50)),
                ('password', models.CharField(max_length=200)),
                ('add_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 705995))),
                ('is_super_admin', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='black_list',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('seller_id', models.IntegerField(default=0)),
                ('black_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 706995))),
            ],
        ),
        migrations.CreateModel(
            name='login_error_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('IP', models.GenericIPAddressField(db_index=True, default='xxx')),
                ('error_times', models.IntegerField(default=0)),
                ('forbid_start_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 707995))),
                ('forbid_end_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 707995))),
            ],
        ),
        migrations.CreateModel(
            name='manage_deal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('buyer_merchant_id', models.IntegerField(db_index=True, default=0)),
                ('seller_merchant_id', models.IntegerField(db_index=True, default=0)),
                ('car_id', models.IntegerField(default=0)),
                ('deal_price', models.FloatField(default=0.0)),
                ('deal_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 706995))),
            ],
        ),
    ]
