# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0025_sampleslayers_density'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('density', models.DecimalField(null=True, max_digits=9, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='CompoundElements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('compound', models.ForeignKey(to='samples_manager.Compound', null=True)),
                ('element_type', models.ForeignKey(to='samples_manager.MaterialElements')),
            ],
        ),
        migrations.RemoveField(
            model_name='sampleselements',
            name='element_type',
        ),
        migrations.RemoveField(
            model_name='sampleselements',
            name='layer',
        ),
        migrations.RemoveField(
            model_name='sampleslayers',
            name='sample',
        ),
        migrations.AlterField(
            model_name='layers',
            name='element_type',
            field=models.ForeignKey(to='samples_manager.MaterialElements', null=True),
        ),
        migrations.DeleteModel(
            name='SamplesElements',
        ),
        migrations.DeleteModel(
            name='SamplesLayers',
        ),
        migrations.AddField(
            model_name='layers',
            name='compound_type',
            field=models.ForeignKey(to='samples_manager.Compound', null=True),
        ),
    ]
