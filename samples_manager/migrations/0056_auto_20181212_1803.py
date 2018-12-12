# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0055_auto_20181212_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradiation',
            name='accumulated_fluence',
            field=models.DecimalField(null=True, max_digits=37, decimal_places=20),
        ),
    ]
