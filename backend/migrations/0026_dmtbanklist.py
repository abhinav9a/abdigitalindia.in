# Generated by Django 4.2.5 on 2024-01-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0025_delete_bank"),
    ]

    operations = [
        migrations.CreateModel(
            name="DMTBankList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bank_name", models.CharField(max_length=255)),
                ("bank_id", models.CharField(max_length=10)),
            ],
        ),
    ]
