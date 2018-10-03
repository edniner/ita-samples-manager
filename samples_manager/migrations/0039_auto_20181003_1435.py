# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0038_userpreferences'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreferences',
            name='theme',
            field=models.CharField(max_length=50),
        ),
    ]
