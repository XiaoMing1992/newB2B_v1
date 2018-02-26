# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='car_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('merchant_id', models.IntegerField(db_index=True, default=0)),
                ('car_type', models.CharField(default='XXX', max_length=100)),
                ('car_brand', models.CharField(default='XXX', max_length=100)),
                ('car_series', models.CharField(default='XXX', max_length=100)),
                ('car_model', models.CharField(default='XXX', max_length=100)),
                ('color', models.CharField(default='XXX', max_length=200)),
                ('color_hex', models.CharField(default='#ffffff', max_length=50)),
                ('delivery_type', models.CharField(default='XXX', max_length=50)),
                ('delivery_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 695994))),
                ('pay_method', models.CharField(default='XXX', max_length=50)),
                ('sell_area', models.CharField(default='XXX', max_length=200)),
                ('method_logistics', models.CharField(default='XXX', max_length=50)),
                ('lowest_price', models.IntegerField(default=0)),
                ('highest_price', models.IntegerField(default=0)),
                ('discount_rate', models.CharField(default='0', max_length=20)),
                ('introduction', models.CharField(default='XXX', max_length=1000)),
                ('date_publish', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 695994))),
                ('date_valid', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 695994))),
                ('read_num', models.IntegerField(default=0)),
                ('province', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('car_type_1', models.IntegerField(default=0)),
                ('car_type_2', models.IntegerField(default=0)),
                ('car_type_3', models.IntegerField(default=0)),
                ('car_type_4', models.IntegerField(default=0)),
                ('color_1', models.IntegerField(default=0)),
                ('color_2', models.IntegerField(default=0)),
                ('color_3', models.IntegerField(default=0)),
                ('color_4', models.IntegerField(default=0)),
                ('color_5', models.IntegerField(default=0)),
                ('color_6', models.IntegerField(default=0)),
                ('color_7', models.IntegerField(default=0)),
                ('is_black', models.IntegerField(default=0)),
                ('black_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 695994))),
            ],
        ),
        migrations.CreateModel(
            name='car_table_people',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('car_id', models.IntegerField(db_index=True, default=0)),
                ('people_name', models.CharField(default='xxx', max_length=100)),
                ('people_phone', models.CharField(default='10086', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='invalid_time_car_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('merchant_id', models.IntegerField(db_index=True, default=0)),
                ('car_style', models.CharField(default='XXX', max_length=100)),
                ('car_brand', models.CharField(default='XXX', max_length=100)),
                ('car_series', models.CharField(default='XXX', max_length=100)),
                ('car_model', models.CharField(default='XXX', max_length=100)),
                ('color', models.CharField(default='XXX', max_length=200)),
                ('color_hex', models.CharField(default='#ffffff', max_length=50)),
                ('delivery_type', models.CharField(default='XXX', max_length=50)),
                ('delivery_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 697994))),
                ('pay_method', models.CharField(default='XXX', max_length=50)),
                ('sell_area', models.CharField(default='XXX', max_length=200)),
                ('method_logistics', models.CharField(default='XXX', max_length=50)),
                ('lowest_price', models.IntegerField(default=0)),
                ('highest_price', models.IntegerField(default=0)),
                ('discount_rate', models.CharField(default='0', max_length=20)),
                ('introduction', models.TextField(default='XXX')),
                ('date_publish', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 697994))),
                ('date_valid', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 697994))),
                ('read_num', models.IntegerField(default=0)),
                ('province', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('car_type_1', models.IntegerField(default=0)),
                ('car_type_2', models.IntegerField(default=0)),
                ('car_type_3', models.IntegerField(default=0)),
                ('car_type_4', models.IntegerField(default=0)),
                ('color_1', models.IntegerField(default=0)),
                ('color_2', models.IntegerField(default=0)),
                ('color_3', models.IntegerField(default=0)),
                ('color_4', models.IntegerField(default=0)),
                ('color_5', models.IntegerField(default=0)),
                ('color_6', models.IntegerField(default=0)),
                ('color_7', models.IntegerField(default=0)),
                ('is_black', models.IntegerField(default=0)),
                ('black_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 697994))),
            ],
        ),
    ]
