# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0036_auto_20180914_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occupancies',
            name='nu_coll_occupancy',
        ),
        migrations.RemoveField(
            model_name='occupancies',
            name='nu_int_occupancy',
        ),
        migrations.AddField(
            model_name='occupancies',
            name='nu_coll_length_occupancy',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='occupancies',
            name='nu_int_length_occupancy',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='occupancies',
            name='radiation_length_occupancy',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=3),
            preserve_default=False,
        ),
    ]
