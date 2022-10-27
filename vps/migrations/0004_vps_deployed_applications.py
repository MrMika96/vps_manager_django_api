# Generated by Django 4.0 on 2022-10-26 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
        ('vps', '0003_vps_maintained_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='vps',
            name='deployed_applications',
            field=models.ManyToManyField(to='applications.Application'),
        ),
    ]