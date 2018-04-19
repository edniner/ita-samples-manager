# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0008_auto_20180418_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samples',
            name='category',
            field=models.CharField(max_length=200),
        ),
    ]
