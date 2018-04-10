# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0002_auto_20180407_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samples',
            name='storage',
            field=models.CharField(max_length=50, choices=[(b'Room temperature', b'Room temperature'), (b'Cold storage <20 \xc2\xb0C', b'Cold storage <20 \xc2\xb0C')]),
        ),
    ]
