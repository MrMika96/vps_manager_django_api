# Generated by Django 4.0 on 2022-10-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vps',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('cpu', models.IntegerField()),
                ('ram', models.IntegerField()),
                ('hdd', models.IntegerField()),
                ('status', models.CharField(choices=[('started', 'started'), ('blocked', 'blocked'), ('stopped', 'stopped')], default='started', max_length=7)),
            ],
        ),
    ]
