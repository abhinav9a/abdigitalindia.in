# Generated by Django 4.2.5 on 2023-12-09 17:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend", "0004_alter_kycinformation_documentname_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="KycInformation",
            new_name="UserKYCDocument",
        ),
    ]
