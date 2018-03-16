# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='irradiation_type',
            field=models.CharField(default='Protons', max_length=100),
            preserve_default=False,
        ),
    ]
