# Generated by Django 4.2.6 on 2023-11-12 17:36

from django.db import migrations


# Generated by Django 4.2.6 on 2023-11-12 17:26
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("applications", "0003_copy_data_to_other_field"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="application",
            name="size",
        ),
        migrations.RenameField(
            model_name="application",
            old_name="size_new",
            new_name="size",
        ),
    ]
