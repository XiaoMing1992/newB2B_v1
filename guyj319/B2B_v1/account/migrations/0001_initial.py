# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='collect_car_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(db_index=True, default=0)),
                ('car_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='collect_seller_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(db_index=True, default=0)),
                ('seller_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='inviteCode_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(db_index=True, default=0)),
                ('receive_phone', models.CharField(default='10086', max_length=15)),
                ('inviteCode', models.CharField(max_length=50, db_index=True, default='xxxxxx')),
                ('validity_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 700994))),
                ('send_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 700994))),
            ],
        ),
        migrations.CreateModel(
            name='message_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('seller_id', models.CharField(default='10086', max_length=15)),
                ('buyer_id', models.CharField(default='10086', max_length=15)),
                ('buyer_search_record_id', models.IntegerField(default=0)),
                ('company_name', models.CharField(default='xxx', max_length=200)),
                ('car_id', models.IntegerField(default=0)),
                ('car_brand', models.CharField(default='XXX', max_length=100)),
                ('car_series', models.CharField(default='XXX', max_length=50)),
                ('car_model', models.CharField(default='XXX', max_length=100)),
                ('message_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 701994))),
                ('tag_type', models.IntegerField(default=3)),
                ('action_type', models.IntegerField(default=2)),
            ],
            options={
                'ordering': ['-message_time'],
            },
        ),
        migrations.CreateModel(
            name='record_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(db_index=True, default=0)),
                ('car_type', models.CharField(default='', max_length=100)),
                ('car_brand', models.CharField(default='', max_length=100)),
                ('car_series', models.CharField(default='', max_length=50)),
                ('car_model', models.CharField(default='', max_length=100)),
                ('color', models.CharField(default='', max_length=200)),
                ('color_hex', models.CharField(default='', max_length=50)),
                ('delivery_type', models.CharField(default='', max_length=50)),
                ('pay_method', models.CharField(default='', max_length=50)),
                ('sell_area', models.CharField(default='', max_length=100)),
                ('method_logistics', models.CharField(default='', max_length=50)),
                ('time_save', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 702995))),
                ('time_valid', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 702995))),
                ('province', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='user_info_people',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('merchant_id', models.IntegerField(default=0)),
                ('user_name', models.CharField(default='xxx', max_length=100)),
                ('user_phone', models.CharField(default='10086', max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='user_info_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(db_index=True, default=0)),
                ('user_company_name', models.CharField(default='xxx', max_length=200)),
                ('user_type', models.CharField(default='xxx', max_length=50)),
                ('user_address', models.CharField(default='xxx', max_length=50)),
                ('user_trademark', models.TextField(default='xxx')),
                ('license_path', models.ImageField(default='temp/5.jpg', upload_to='license/')),
                ('id_card_path', models.ImageField(default='temp/5.jpg', upload_to='id_card/')),
                ('head_icon_path', models.ImageField(default='temp/5.jpg', upload_to='head_icon/')),
                ('province', models.CharField(default='', max_length=50)),
                ('city', models.CharField(default='', max_length=50)),
                ('is_black', models.IntegerField(default=0)),
                ('black_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 703995))),
                ('add_time', models.DateTimeField(default=datetime.datetime(2016, 12, 6, 21, 15, 43, 703995))),
                ('state', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='user_more_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('seller_id', models.IntegerField(db_index=True, default=0)),
                ('collect_people_num', models.IntegerField(default=0)),
                ('valid_publish_num', models.IntegerField(default=0)),
            ],
        ),
    ]
