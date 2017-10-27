# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0004_samples'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dosimeters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dosimeter_id', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=50)),
                ('weight', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('foils_number', models.CharField(max_length=50)),
                ('density', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('comments', models.TextField()),
            ],
        ),
    ]
