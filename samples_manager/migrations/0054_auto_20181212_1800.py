# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0053_auto_20181212_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradiation',
            name='accumulated_fluence',
            field=models.DecimalField(null=True, max_digits=40, decimal_places=20),
        ),
    ]
