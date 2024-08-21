# Generated by Django 4.2.5 on 2024-01-26 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend", "0044_delete_payout"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payout",
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
                (
                    "amount",
                    models.CharField(blank=True, max_length=500, verbose_name="Amount"),
                ),
                (
                    "txn_status",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Txn Status"
                    ),
                ),
                (
                    "tid",
                    models.CharField(blank=True, max_length=500, verbose_name="Tid"),
                ),
                (
                    "client_ref_id",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="Client Ref Id"
                    ),
                ),
                (
                    "recipient_name",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="Recipient Name"
                    ),
                ),
                (
                    "ifsc",
                    models.CharField(blank=True, max_length=500, verbose_name="IFSC"),
                ),
                (
                    "account",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="Account"
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "userAccount",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Linked User",
                    ),
                ),
            ],
        ),
    ]
