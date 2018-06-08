# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0022_auto_20180608_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='irrad_ps_user',
        ),
    ]
