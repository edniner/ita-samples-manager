# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='samples',
            old_name='description',
            new_name='name',
        ),
    ]
