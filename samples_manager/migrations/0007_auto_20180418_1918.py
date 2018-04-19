# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0006_auto_20180410_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dosimeters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dos_id', models.CharField(max_length=50, unique=True, null=True)),
                ('current_location', models.CharField(max_length=100)),
                ('length', models.DecimalField(max_digits=12, decimal_places=3)),
                ('height', models.DecimalField(max_digits=12, decimal_places=3)),
                ('width', models.DecimalField(max_digits=12, decimal_places=3)),
                ('weight', models.DecimalField(null=True, max_digits=12, decimal_places=3)),
                ('foils_number', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'InBeam', b'In beam'), (b'OutBeam', b'Out of beam'), (b'CoolingDown', b'Cooling down'), (b'Completed', b'Completed'), (b'InStorage', b'In Storage'), (b'OutOfIRRAD', b'Out of IRRAD'), (b'Waste', b'Waste')])),
                ('dos_type', models.CharField(max_length=50, choices=[(b'Aluminium', b'Aluminium'), (b'Film', b'Film'), (b'Diamond', b'Diamond'), (b'Other', b'Other')])),
                ('comments', models.TextField(null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('last_location', models.CharField(max_length=100)),
                ('box', models.ForeignKey(to='samples_manager.Boxes', null=True)),
                ('created_by', models.ForeignKey(related_name='dosimeters_created_by', to='samples_manager.Users', null=True)),
                ('responsible', models.ForeignKey(related_name='dosimeters_responsible', to='samples_manager.Users')),
                ('updated_by', models.ForeignKey(related_name='dosimeters_updated_by', to='samples_manager.Users', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='layers',
            name='length',
            field=models.DecimalField(max_digits=26, decimal_places=6),
        ),
        migrations.AlterField(
            model_name='layers',
            name='percentage',
            field=models.DecimalField(max_digits=8, decimal_places=4),
        ),
    ]
