# Generated by Django 2.1.7 on 2019-03-13 14:03

import django.contrib.sites.managers
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('station', '0003_spareproxy'),
    ]

    operations = [
        migrations.CreateModel(
            name='CivilNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('serial', models.CharField(choices=[('AA', 'Kiev'), ('AH', 'Donetsk')], default='AA', max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MilitaryNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('serial', models.CharField(choices=[('B1', 'Military law enforcement service of the AFU'), ('E1', 'Military units of engineering troops of the AFU')], default='E1', max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='PassengerСar',
            fields=[
                ('transport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='station.Transport')),
                ('hatch', models.BooleanField(default=False)),
                ('seats', models.IntegerField(default=2)),
            ],
            bases=('station.transport',),
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('transport_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='station.Transport')),
                ('lifting_gear', models.BooleanField(default=False)),
                ('pallet_places', models.IntegerField(default=2)),
                ('height', models.FloatField(default='1.0')),
                ('width', models.FloatField(default='1.0')),
            ],
            bases=('station.transport',),
        ),
        migrations.AlterModelOptions(
            name='spareproxy',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelManagers(
            name='color',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.AddField(
            model_name='color',
            name='sites',
            field=models.ManyToManyField(to='sites.Site'),
        ),
    ]
