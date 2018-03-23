# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0002_auto_20180322_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleselements',
            name='sample',
            field=models.ForeignKey(to='samples_manager.Samples', null=True),
        ),
    ]
