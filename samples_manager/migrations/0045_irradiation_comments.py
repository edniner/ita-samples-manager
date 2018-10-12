# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0044_auto_20181010_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='irradiation',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]
