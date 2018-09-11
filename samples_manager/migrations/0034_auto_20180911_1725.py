# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('samples_manager', '0033_archiveexperimentsample_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Irradiation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_in', models.DateTimeField(null=True, blank=True)),
                ('date_out', models.DateTimeField(null=True, blank=True)),
                ('table_position', models.CharField(max_length=50, null=True)),
                ('irrad_table', models.CharField(max_length=50)),
                ('accumulated_fluence', models.DecimalField(null=True, max_digits=30, decimal_places=6)),
                ('created_at', models.DateTimeField(null=True, editable=False)),
                ('updated_at', models.DateTimeField(null=True)),
                ('status', models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'InBeam', b'In beam'), (b'OutBeam', b'Out of beam'), (b'CoolingDown', b'Cooling down'), (b'Completed', b'Completed'), (b'InStorage', b'In Storage'), (b'OutOfIRRAD', b'Out of IRRAD'), (b'Waste', b'Waste')])),
                ('created_by', models.ForeignKey(related_name='irradiation_created_by', to='samples_manager.Users', null=True)),
                ('dosimeter', models.ForeignKey(to='samples_manager.Dosimeters', null=True)),
                ('sample', models.ForeignKey(to='samples_manager.Samples', null=True)),
                ('updated_by', models.ForeignKey(related_name='irradiation_updated_by', to='samples_manager.Users', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='irradation',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='irradation',
            name='dosimeter',
        ),
        migrations.RemoveField(
            model_name='irradation',
            name='sample',
        ),
        migrations.RemoveField(
            model_name='irradation',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Irradation',
        ),
    ]
