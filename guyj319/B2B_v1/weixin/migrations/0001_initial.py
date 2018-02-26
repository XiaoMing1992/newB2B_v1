# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='weiXinUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('openid', models.CharField(db_index=True, max_length=100)),
                ('phone', models.CharField(max_length=15, db_index=True, default='10086')),
                ('state', models.IntegerField(default=0)),
            ],
        ),
    ]
