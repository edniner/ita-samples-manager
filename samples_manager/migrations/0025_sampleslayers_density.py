# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0024_users_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleslayers',
            name='density',
            field=models.DecimalField(null=True, max_digits=9, decimal_places=3),
        ),
    ]
