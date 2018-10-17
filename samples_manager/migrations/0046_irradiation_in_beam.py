# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0045_irradiation_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='irradiation',
            name='in_beam',
            field=models.BooleanField(default=False),
        ),
    ]
