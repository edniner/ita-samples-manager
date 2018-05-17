# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0013_auto_20180507_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Irradation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_in', models.DateTimeField(null=True, blank=True)),
                ('date_out', models.DateTimeField(null=True, blank=True)),
                ('position', models.CharField(max_length=50)),
                ('accumulated_fluence', models.DecimalField(max_digits=30, decimal_places=6)),
                ('dosimeter', models.ForeignKey(to='samples_manager.Dosimeters', null=True)),
                ('sample', models.ForeignKey(to='samples_manager.Samples', null=True)),
            ],
        ),
    ]
