# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20170705_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='uu',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
