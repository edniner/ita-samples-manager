# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0003_experusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Samples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_id', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=50)),
                ('weight', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('requested_fluence', models.CharField(max_length=50)),
                ('cern_experiment', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('comments', models.TextField()),
                ('experiment_id', models.ForeignKey(to='samples_manager.Experiments')),
            ],
        ),
    ]
