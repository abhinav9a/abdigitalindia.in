# Generated by Django 4.2.5 on 2024-01-19 15:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0038_commission"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commission",
            name="AepsCommission",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Aeps Commission",
            ),
        ),
        migrations.AlterField(
            model_name="commission",
            name="DmtCommission",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="DMT Commission",
            ),
        ),
    ]
