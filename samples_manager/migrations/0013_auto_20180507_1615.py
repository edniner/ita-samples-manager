# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0012_auto_20180504_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosimeters',
            name='current_location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='foils_number',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='height',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='last_location',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='length',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='responsible',
            field=models.ForeignKey(related_name='dosimeters_responsible', to='samples_manager.Users', null=True),
        ),
        migrations.AlterField(
            model_name='dosimeters',
            name='width',
            field=models.DecimalField(null=True, max_digits=18, decimal_places=6),
        ),
    ]
