# Generated by Django 4.2.5 on 2023-12-26 14:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0021_alter_aepstxncallbackbyeko_tx_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aepstxncallbackbyeko",
            name="user_code",
        ),
    ]
