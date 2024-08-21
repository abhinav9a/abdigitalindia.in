# Generated by Django 4.2.5 on 2024-03-14 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "backend",
            "0060_rename_bbpshcwaterngas1_commission_bbpshcwaterngasslab1_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="commission",
            name="BbpsHCAirtelMobilePrepaid",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Airtel Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCAirtelMobilePrepaidDistributor",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Distributor Airtel Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCAirtelMobilePrepaidMaster",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Master Airtel Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCBSNLMobilePrepaid",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission BSNL Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCBSNLMobilePrepaidDistributor",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Distributor BSNL Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCBSNLMobilePrepaidMaster",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Master BSNL Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCJioMobilePrepaid",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission JIO Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCJioMobilePrepaidDistributor",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Distributor JIO Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCJioMobilePrepaidMaster",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Master JIO Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCMTNLMobilePrepaid",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission MTNL Delhi & Mumbai Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCMTNLMobilePrepaidDistributor",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Distributor MTNL Delhi & Mumbai Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCMTNLMobilePrepaidMaster",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Master MTNL Delhi & Mumbai Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCVIMobilePrepaid",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission VI Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCVIMobilePrepaidDistributor",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Distributor VI Mobile Prepaid - Any Amount (%)",
            ),
        ),
        migrations.AddField(
            model_name="commission",
            name="BbpsHCVIMobilePrepaidMaster",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=10,
                verbose_name="High Commission Master VI Mobile Prepaid - Any Amount (%)",
            ),
        ),
    ]
