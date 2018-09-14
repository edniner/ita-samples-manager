# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0035_occupancies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occupancies',
            name='nu_coll_occupancy',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='occupancies',
            name='nu_int_occupancy',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='occupancies',
            name='radiation_length_occupancy',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3),
        ),
    ]
