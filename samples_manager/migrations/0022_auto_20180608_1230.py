# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0021_auto_20180608_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='users',
            old_name='ps_irrad_user',
            new_name='irrad_ps_user',
        ),
    ]
