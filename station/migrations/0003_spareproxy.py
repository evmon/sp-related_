# Generated by Django 2.1.7 on 2019-03-11 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0002_delete_passport'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpareProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('station.spare',),
        ),
    ]
