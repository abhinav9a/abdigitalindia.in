# Generated by Django 4.2.5 on 2023-12-24 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend", "0016_rename_servicestatus_serviceactivation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="serviceactivation",
            name="userAccount",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
