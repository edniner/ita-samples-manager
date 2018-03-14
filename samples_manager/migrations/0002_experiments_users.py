# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiments',
            name='users',
            field=models.ManyToManyField(to='samples_manager.Users'),
        ),
    ]
