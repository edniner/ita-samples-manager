# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0005_auto_20180410_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='samples',
            name='storage',
            field=models.CharField(max_length=50, choices=[(b'Room temperature', b'Room temperature'), (b'Cold storage <20', b'Cold storage <20 \xc2\xb0C')]),
        ),
    ]
