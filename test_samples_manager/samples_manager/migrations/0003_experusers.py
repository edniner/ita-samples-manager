# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0002_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('irradiation_id', models.ForeignKey(to='samples_manager.Experiments')),
                ('user_id', models.ForeignKey(to='samples_manager.Users')),
            ],
        ),
    ]
