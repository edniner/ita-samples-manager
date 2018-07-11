# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0026_auto_20180709_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layers',
            name='percentage',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=4),
        ),
    ]
