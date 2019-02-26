# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0058_auto_20190121_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradiation',
            name='dos_position',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
