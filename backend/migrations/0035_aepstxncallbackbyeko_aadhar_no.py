# Generated by Django 4.2.5 on 2024-01-10 18:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0034_aepstxncallbackbyeko_tid"),
    ]

    operations = [
        migrations.AddField(
            model_name="aepstxncallbackbyeko",
            name="aadhar_no",
            field=models.CharField(
                blank=True, max_length=500, verbose_name="aadhar_no"
            ),
        ),
    ]
