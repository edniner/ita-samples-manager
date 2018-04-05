# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


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
                ('number_samples', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('comments', models.TextField(null=True)),
                ('category', models.CharField(max_length=100, choices=[(b'', b'Please,choose category'), (b'Passive Standard', b'Passive Standard'), (b'Passive Custom', b'Passive Custom'), (b'Active', b'Active')])),
                ('regulations_flag', models.BooleanField()),
                ('irradiation_type', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'OnGoing', b'On going'), (b'Paused', b'Paused'), (b'Completed', b'Completed')])),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Layers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('length', models.DecimalField(max_digits=20, decimal_places=6)),
                ('percentage', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='MaterialElements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('atomic_number', models.PositiveIntegerField()),
                ('atomic_symbol', models.CharField(max_length=5)),
                ('atomic_mass', models.DecimalField(max_digits=15, decimal_places=10)),
                ('density', models.DecimalField(max_digits=9, decimal_places=7)),
                ('min_ionization', models.DecimalField(max_digits=4, decimal_places=3)),
                ('nu_coll_length', models.DecimalField(max_digits=4, decimal_places=1)),
                ('nu_int_length', models.DecimalField(max_digits=4, decimal_places=1)),
                ('pi_coll_length', models.DecimalField(max_digits=4, decimal_places=1)),
                ('pi_int_length', models.DecimalField(max_digits=4, decimal_places=1)),
                ('radiation_length', models.DecimalField(max_digits=4, decimal_places=2)),
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
            name='Samples',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_id', models.CharField(max_length=50, unique=True, null=True)),
                ('description', models.CharField(unique=True, max_length=200)),
                ('current_location', models.CharField(max_length=100)),
                ('height', models.DecimalField(max_digits=12, decimal_places=6)),
                ('width', models.DecimalField(max_digits=12, decimal_places=6)),
                ('weight', models.DecimalField(null=True, max_digits=12, decimal_places=6)),
                ('comments', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('storage', models.CharField(max_length=50, choices=[(b'Room', b'Room temperature'), (b'Cold', b'Cold storage <20 \xc2\xb0C')])),
                ('status', models.CharField(max_length=50, choices=[(b'Registered', b'Registered'), (b'Updated', b'Updated'), (b'Approved', b'Approved'), (b'Ready', b'Ready'), (b'InBeam', b'In beam'), (b'OutBeam', b'Out of beam'), (b'CoolingDown', b'Cooling down'), (b'Completed', b'Completed'), (b'InStorage', b'In Storage'), (b'OutOfIRRAD', b'Out of IRRAD'), (b'Waste', b'Waste')])),
                ('last_location', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('box', models.ForeignKey(to='samples_manager.Boxes', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SamplesElements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('element_type', models.ForeignKey(to='samples_manager.MaterialElements')),
            ],
        ),
        migrations.CreateModel(
            name='SamplesLayers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('length', models.DecimalField(max_digits=20, decimal_places=6)),
                ('sample', models.ForeignKey(to='samples_manager.Samples', null=True)),
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
            model_name='sampleselements',
            name='layer',
            field=models.ForeignKey(to='samples_manager.SamplesLayers', null=True),
        ),
        migrations.AddField(
            model_name='samples',
            name='created_by',
            field=models.ForeignKey(related_name='samples_created_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='samples',
            name='experiment',
            field=models.ForeignKey(to='samples_manager.Experiments', null=True),
        ),
        migrations.AddField(
            model_name='samples',
            name='material',
            field=models.ForeignKey(to='samples_manager.Materials'),
        ),
        migrations.AddField(
            model_name='samples',
            name='req_fluence',
            field=models.ForeignKey(to='samples_manager.ReqFluences'),
        ),
        migrations.AddField(
            model_name='samples',
            name='updated_by',
            field=models.ForeignKey(related_name='samples_updated_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='layers',
            name='element_type',
            field=models.ForeignKey(to='samples_manager.MaterialElements'),
        ),
        migrations.AddField(
            model_name='layers',
            name='sample',
            field=models.ForeignKey(to='samples_manager.Samples', null=True),
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
            model_name='experiments',
            name='users',
            field=models.ManyToManyField(to='samples_manager.Users'),
        ),
        migrations.AddField(
            model_name='boxes',
            name='created_by',
            field=models.ForeignKey(related_name='boxes_created_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='boxes',
            name='responsible',
            field=models.ForeignKey(related_name='boxes_responsible', to='samples_manager.Users'),
        ),
        migrations.AddField(
            model_name='boxes',
            name='updated_by',
            field=models.ForeignKey(related_name='boxes_updated_by', to='samples_manager.Users', null=True),
        ),
        migrations.AddField(
            model_name='activecategories',
            name='experiment',
            field=models.ForeignKey(to='samples_manager.Experiments', null=True),
        ),
    ]
