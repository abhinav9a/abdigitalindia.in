# Generated by Django 4.2.5 on 2023-12-10 12:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_useraccount_unique_sequence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useraccount",
            name="unique_sequence",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Unique sequence"
            ),
        ),
    ]
