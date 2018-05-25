# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0014_irradation'),
    ]

    operations = [
        migrations.AddField(
            model_name='irradation',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 25, 14, 26, 11, 206000, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irradation',
            name='created_by',
            field=models.ForeignKey(related_name='irradation_created_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='irradation',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 5, 25, 14, 26, 25, 351000, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='irradation',
            name='updated_by',
            field=models.ForeignKey(related_name='irradation_updated_by', to='samples_manager.Users', null=True),
        ),
    ]
