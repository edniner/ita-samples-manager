# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0054_auto_20181212_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradiation',
            name='accumulated_fluence',
            field=models.DecimalField(null=True, max_digits=38, decimal_places=14),
        ),
    ]
