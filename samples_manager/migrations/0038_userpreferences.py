# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0037_auto_20180914_1307'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('theme', models.CharField(max_length=50, choices=[(b'amazon', b'amazon'), (b'bookish', b'bookish'), (b'chubby', b'chubby'), (b'colored', b'colored'), (b'default', b'default'), (b'round', b'round'), (b'github', b'github'), (b'material', b'material'), (b'flat', b'flat')])),
                ('user', models.ForeignKey(to='samples_manager.Users', null=True)),
            ],
        ),
    ]
