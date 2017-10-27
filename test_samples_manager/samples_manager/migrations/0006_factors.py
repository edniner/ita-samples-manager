# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0005_dosimeters'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('samples_size', models.CharField(max_length=50)),
                ('material', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
            ],
        ),
    ]
