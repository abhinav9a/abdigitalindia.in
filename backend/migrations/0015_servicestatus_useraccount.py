# Generated by Django 4.2.5 on 2023-12-24 10:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend", "0014_servicestatus"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicestatus",
            name="userAccount",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Linked User",
            ),
            preserve_default=False,
        ),
    ]
