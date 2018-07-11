# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0029_auto_20180711_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compound',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
