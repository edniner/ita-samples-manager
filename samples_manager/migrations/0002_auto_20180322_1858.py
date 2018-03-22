# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samples',
            name='weight',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=6),
        ),
    ]
