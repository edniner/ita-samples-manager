# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0032_archiveexperimentsample'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveexperimentsample',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 3, 15, 55, 46, 352000, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]
