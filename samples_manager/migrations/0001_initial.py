# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import samples_manager.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active_category_type', models.CharField(max_length=50)),
                ('active_irradiation_area', models.CharField(max_length=50)),
                ('active_modus_operandi', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Experiments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('description', models.TextField()),
                ('cern_experiment', models.CharField(max_length=100)),
                ('availability', models.DateField(null=True)),
                ('constraints', models.CharField(max_length=2000)),
                ('number_samples', models.PositiveIntegerField(default=0, validators=[samples_manager.models.validate_negative])),
                ('comments', models.TextField(null=True)),
                ('category', models.CharField(max_length=100, choices=[(b'', b'Please,choose category'), (b'Passive Standard', b'Passive Standard'), (b'Passive Custom', b'Passive Custom'), (b'Active', b'Active')])),
                ('regulations_flag', models.BooleanField()),
                ('status', models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'OnGoing', b'On going'), (b'Paused', b'Paused'), (b'Completed', b'Completed')])),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Materials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('material', models.CharField(max_length=50)),
                ('experiment', models.ForeignKey(to='samples_manager.Experiments', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PassiveCustomCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('passive_category_type', models.CharField(max_length=50)),
                ('passive_irradiation_area', models.CharField(max_length=50)),
                ('passive_modus_operandi', models.TextField()),
                ('experiment', models.ForeignKey(to='samples_manager.Experiments', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PassiveStandardCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('irradiation_area_5x5', models.BooleanField()),
                ('irradiation_area_10x10', models.BooleanField()),
                ('irradiation_area_20x20', models.BooleanField()),
                ('experiment', models.ForeignKey(to='samples_manager.Experiments', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReqFluences',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('req_fluence', models.CharField(max_length=50)),
                ('experiment', models.ForeignKey(to='samples_manager.Experiments', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=200)),
                ('name', models.CharField(max_length=200, null=True)),
                ('surname', models.CharField(max_length=200, null=True)),
                ('telephone', models.CharField(max_length=200, null=True)),
                ('role', models.CharField(default=b'Basic User', max_length=100, null=True, choices=[(b'Owner', b'Owner'), (b'Operator', b'Operator'), (b'Cordinator', b'Cordinator'), (b'Basic', b'Basic User')])),
            ],
        ),
        migrations.AddField(
            model_name='experiments',
            name='created_by',
            field=models.ForeignKey(related_name='experiments_created_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='experiments',
            name='responsible',
            field=models.ForeignKey(related_name='experiments_responsible', to='samples_manager.Users'),
        ),
        migrations.AddField(
            model_name='experiments',
            name='updated_by',
            field=models.ForeignKey(related_name='experiments_updated_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='activecategories',
            name='experiment',
            field=models.ForeignKey(to='samples_manager.Experiments', null=True),
        ),
    ]
