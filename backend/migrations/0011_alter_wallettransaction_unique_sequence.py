# Generated by Django 4.2.5 on 2023-12-14 16:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0010_wallettransaction_unique_sequence"),
    ]

    operations = [
        migrations.AlterField(
            model_name="wallettransaction",
            name="unique_sequence",
            field=models.IntegerField(
                blank=True, default=0, null=True, verbose_name="Unique sequence"
            ),
        ),
    ]
