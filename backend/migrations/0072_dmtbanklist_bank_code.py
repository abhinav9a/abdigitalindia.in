# Generated by Django 4.2.5 on 2024-04-21 11:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0071_remove_creditcardtxn_commission"),
    ]

    operations = [
        migrations.AddField(
            model_name="dmtbanklist",
            name="bank_code",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
