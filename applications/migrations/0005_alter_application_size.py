# Generated by Django 4.2.6 on 2023-11-12 18:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("applications", "0004_remove_application_size_new_alter_application_size"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="size",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
