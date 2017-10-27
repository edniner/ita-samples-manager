# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Experiments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('max_requested_fluence', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('justification', models.TextField(verbose_name=b'Justification (if any)')),
                ('resources', models.TextField()),
                ('storage', models.CharField(max_length=100)),
                ('irradiation_type', models.CharField(max_length=100, choices=[(b'PASSIVE', b'Passive'), (b'ACTIVE', b'Active')])),
                ('category', models.CharField(max_length=100, choices=[(b'5x5', b'5x5'), (b'10x10', b'10x10'), (b'20x20', b'20x20'), (b'Cold irradiation', b'Cold irradiation'), (b'Cryogenics', b'Cryogenics'), (b'Scanning', b'Scanning'), (b'Big setup', b'Big setup'), (b'Other', b'Other')])),
                ('regulations_flag', models.BooleanField()),
                ('planning', models.TextField()),
            ],
        ),
    ]
