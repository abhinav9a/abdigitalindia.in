# Generated by Django 4.2.5 on 2024-03-03 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("backend", "0052_dmttxn_account_dmttxn_bank_dmttxn_bank_ref_num_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor1",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Distributor Aeps 100-199 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor2",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Distributor Aeps 200-999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor3",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Distributor Aeps 1000-1499 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor4",
            field=models.DecimalField(
                decimal_places=2,
                default=1.0,
                max_digits=5,
                verbose_name="Distributor Aeps 1500-1999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor5",
            field=models.DecimalField(
                decimal_places=2,
                default=1.0,
                max_digits=5,
                verbose_name="Distributor Aeps 2000-2499 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor6",
            field=models.DecimalField(
                decimal_places=2,
                default=1.0,
                max_digits=5,
                verbose_name="Distributor Aeps 2500-2999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor7",
            field=models.DecimalField(
                decimal_places=2,
                default=1.0,
                max_digits=5,
                verbose_name="Distributor Aeps 3000-7999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabDistributor8",
            field=models.DecimalField(
                decimal_places=2,
                default=1.0,
                max_digits=5,
                verbose_name="Distributor Aeps 8000 & above (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster1",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Master Distributor Aeps 100-199 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster2",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Master Distributor Aeps 200-999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster3",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=5,
                verbose_name="Master Distributor Aeps 1000-1499 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster4",
            field=models.DecimalField(
                decimal_places=2,
                default=0.5,
                max_digits=5,
                verbose_name="Master Distributor Aeps 1500-1999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster5",
            field=models.DecimalField(
                decimal_places=2,
                default=0.5,
                max_digits=5,
                verbose_name="Master Distributor Aeps 2000-2499 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster6",
            field=models.DecimalField(
                decimal_places=2,
                default=0.5,
                max_digits=5,
                verbose_name="Master Distributor Aeps 2500-2999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster7",
            field=models.DecimalField(
                decimal_places=2,
                default=0.5,
                max_digits=5,
                verbose_name="Master Distributor Aeps 3000-7999 (Rs)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="AepsCommissionSlabMaster8",
            field=models.DecimalField(
                decimal_places=2,
                default=0.5,
                max_digits=5,
                verbose_name="Master Distributor Aeps 8000 & above (Rs)",
            ),
        ),
        migrations.AlterField(
            model_name="commission",
            name="userAccount",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Linked User",
            ),
        ),
        migrations.AlterField(
            model_name="userkycdocument",
            name="userAccount",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Linked User",
            ),
        ),
        migrations.CreateModel(
            name="CommissionTxn",
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
                    "desc",
                    models.CharField(
                        max_length=50, verbose_name="Commission Description"
                    ),
                ),
                (
                    "agent_name",
                    models.CharField(
                        blank=True, max_length=500, verbose_name="Agent Name"
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
