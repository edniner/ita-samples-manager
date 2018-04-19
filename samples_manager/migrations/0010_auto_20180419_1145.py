# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0009_auto_20180418_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosimeters',
            name='dos_type',
            field=models.CharField(max_length=50, choices=[(b'', b''), (b'Aluminium', b'Aluminium'), (b'Film', b'Film'), (b'Diamond', b'Diamond'), (b'Other', b'Other')]),
        ),
    ]
