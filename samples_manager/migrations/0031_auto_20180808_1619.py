# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0030_auto_20180711_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compoundelements',
            name='percentage',
            field=models.DecimalField(max_digits=15, decimal_places=4),
        ),
    ]
