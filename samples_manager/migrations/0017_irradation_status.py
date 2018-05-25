# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0016_auto_20180525_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='irradation',
            name='status',
            field=models.CharField(default='', max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'InBeam', b'In beam'), (b'OutBeam', b'Out of beam'), (b'CoolingDown', b'Cooling down'), (b'Completed', b'Completed'), (b'InStorage', b'In Storage'), (b'OutOfIRRAD', b'Out of IRRAD'), (b'Waste', b'Waste')]),
            preserve_default=False,
        ),
    ]
