# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0015_auto_20180525_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irradation',
            name='accumulated_fluence',
            field=models.DecimalField(null=True, max_digits=30, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='irradation',
            name='created_at',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='irradation',
            name='position',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='irradation',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]
