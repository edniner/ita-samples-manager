# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0023_remove_users_irrad_ps_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 8, 13, 7, 52, 77000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
