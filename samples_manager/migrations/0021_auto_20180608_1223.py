# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0020_auto_20180608_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='group',
        ),
        migrations.AddField(
            model_name='users',
            name='ps_irrad_user',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
