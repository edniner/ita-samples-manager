# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0048_auto_20181107_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradiation',
            name='in_beam',
            field=models.BooleanField(default=False),
        ),
    ]
