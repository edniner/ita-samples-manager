# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0011_auto_20180419_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosimeters',
            name='weight',
            field=models.DecimalField(null=True, max_digits=21, decimal_places=9),
        ),
        migrations.AlterField(
            model_name='experiments',
            name='status',
            field=models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Validated', b'Validated'), (b'On going', b'On going'), (b'Paused', b'Paused'), (b'Completed', b'Completed')]),
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.CharField(default=b'User', max_length=100, null=True, choices=[(b'Owner', b'Owner'), (b'Operator', b'Operator'), (b'Coordinator', b'Coordinator'), (b'User', b'User')]),
        ),
    ]
