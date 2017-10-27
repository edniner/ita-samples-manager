# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0006_factors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Irradiations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_in', models.DateTimeField(null=True, blank=True)),
                ('date_out', models.DateTimeField(null=True, blank=True)),
                ('position', models.CharField(max_length=50)),
                ('sec_in', models.BigIntegerField()),
                ('sec_out', models.BigIntegerField()),
                ('dosimeters_id', models.ForeignKey(to='samples_manager.Dosimeters')),
                ('samples_id', models.ForeignKey(to='samples_manager.Samples')),
            ],
        ),
    ]
