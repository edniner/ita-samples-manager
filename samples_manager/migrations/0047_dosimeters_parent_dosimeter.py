# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0046_irradiation_in_beam'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosimeters',
            name='parent_dosimeter',
            field=models.ForeignKey(to='samples_manager.Dosimeters', null=True),
        ),
    ]
