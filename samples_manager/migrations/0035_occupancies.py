# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0034_auto_20180911_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occupancies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('radiation_length_occupancy', models.DecimalField(max_digits=9, decimal_places=3)),
                ('nu_coll_occupancy', models.DecimalField(max_digits=9, decimal_places=3)),
                ('nu_int_occupancy', models.DecimalField(max_digits=9, decimal_places=3)),
                ('sample', models.ForeignKey(to='samples_manager.Samples', null=True)),
            ],
        ),
    ]
