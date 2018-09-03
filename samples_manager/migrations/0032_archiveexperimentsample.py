# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0031_auto_20180808_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveExperimentSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('experiment', models.ForeignKey(to='samples_manager.Experiments', null=True)),
                ('sample', models.ForeignKey(to='samples_manager.Samples', null=True)),
            ],
        ),
    ]
