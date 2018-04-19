# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0007_auto_20180418_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosimeters',
            name='height',
            field=models.DecimalField(max_digits=18, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='length',
            field=models.DecimalField(max_digits=18, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='weight',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='width',
            field=models.DecimalField(max_digits=18, decimal_places=6),
        ),
    ]
