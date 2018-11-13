# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0049_auto_20181108_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradiation',
            name='in_beam',
            field=models.BooleanField(),
        ),
    ]
