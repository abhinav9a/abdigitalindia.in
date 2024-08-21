# Generated by Django 4.2.7 on 2024-03-15 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0064_commission_bbpshcdthbigtv_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CMSTxnCallbackByEko',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_status', models.CharField(blank=True, max_length=20)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Amount')),
                ('client_ref_id', models.CharField(max_length=500, verbose_name='client_ref_id')),
                ('tid', models.CharField(blank=True, max_length=500, verbose_name='tid')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('commission', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Commission')),
                ('txn_detail', models.JSONField(verbose_name='Transaction JSON')),
                ('userAccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Linked User')),
            ],
        ),
    ]
