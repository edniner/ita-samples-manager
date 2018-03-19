# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0002_experiments_irradiation_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boxes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('box_id', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200, null=True)),
                ('current_location', models.CharField(max_length=100)),
                ('last_location', models.CharField(max_length=100)),
                ('length', models.CharField(max_length=50)),
                ('height', models.CharField(max_length=50)),
                ('width', models.CharField(max_length=50)),
                ('weight', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('created_by', models.ForeignKey(related_name='boxes_created_by', to='samples_manager.Users', null=True)),
                ('responsible', models.ForeignKey(related_name='boxes_responsible', to='samples_manager.Users')),
                ('updated_by', models.ForeignKey(related_name='boxes_updated_by', to='samples_manager.Users', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Samples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_id', models.CharField(max_length=50, unique=True, null=True)),
                ('description', models.CharField(unique=True, max_length=200)),
                ('current_location', models.CharField(max_length=100)),
                ('length', models.CharField(max_length=50)),
                ('height', models.CharField(max_length=50)),
                ('width', models.CharField(max_length=50)),
                ('weight', models.CharField(max_length=50)),
                ('comments', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('storage', models.CharField(max_length=50, choices=[(b'Room', b'Room temperature'), (b'Cold', b'Cold storage <20 \xc2\xb0C')])),
                ('status', models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'InBeam', b'In beam'), (b'OutBeam', b'Out of beam'), (b'CoolingDown', b'Cooling down'), (b'Completed', b'Completed'), (b'InStorage', b'In Storage'), (b'OutOfIRRAD', b'Out of IRRAD'), (b'Waste', b'Waste')])),
                ('last_location', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('box', models.ForeignKey(to='samples_manager.Boxes', null=True)),
                ('created_by', models.ForeignKey(related_name='samples_created_by', to='samples_manager.Users', null=True)),
                ('experiment', models.ForeignKey(to='samples_manager.Experiments', null=True)),
                ('material', models.ForeignKey(to='samples_manager.Materials')),
                ('req_fluence', models.ForeignKey(to='samples_manager.ReqFluences')),
                ('updated_by', models.ForeignKey(related_name='samples_updated_by', to='samples_manager.Users', null=True)),
            ],
        ),
    ]
