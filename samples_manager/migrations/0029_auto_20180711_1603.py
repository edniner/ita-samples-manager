# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0028_auto_20180711_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compound',
            name='density',
            field=models.DecimalField(null=True, max_digits=16, decimal_places=7),
        ),
    ]
