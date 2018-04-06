# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layers',
            name='density',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='layers',
            name='length',
            field=models.DecimalField(max_digits=20, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='layers',
            name='percentage',
            field=models.DecimalField(max_digits=4, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='samples',
            name='height',
            field=models.DecimalField(max_digits=12, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='samples',
            name='weight',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='samples',
            name='width',
            field=models.DecimalField(max_digits=12, decimal_places=3),
        ),
    ]
