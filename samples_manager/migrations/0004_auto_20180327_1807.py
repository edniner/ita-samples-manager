# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0003_auto_20180323_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='SamplesLayers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('length', models.DecimalField(max_digits=20, decimal_places=6)),
                ('sample', models.ForeignKey(to='samples_manager.Samples', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sampleselements',
            name='element_length',
        ),
        migrations.AddField(
            model_name='sampleselements',
            name='percentage',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='sampleselements',
            name='sample',
            field=models.ForeignKey(to='samples_manager.SamplesLayers', null=True),
        ),
    ]
