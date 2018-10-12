# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0043_userpreferences_table_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='irradiation',
            name='fluence_error',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=3),
        ),
        migrations.AddField(
            model_name='irradiation',
            name='sec',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='irradiation',
            name='irrad_table',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
