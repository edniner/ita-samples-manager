# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0050_auto_20181108_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='public_experiment',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
