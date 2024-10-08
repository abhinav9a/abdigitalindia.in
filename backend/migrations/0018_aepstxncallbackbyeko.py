# Generated by Django 4.2.7 on 2023-12-25 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0017_alter_serviceactivation_useraccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='AepsTxnCallbackByEko',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.CharField(max_length=50, verbose_name='user code')),
                ('tx_status', models.CharField(choices=[('P', 'Pending'), ('S', 'Success'), ('C', 'Cancel')], default='P', max_length=20)),
                ('client_ref_id', models.CharField(max_length=500, verbose_name='client_ref_id')),
                ('amount', models.CharField(max_length=50, verbose_name='amount')),
                ('service_type', models.CharField(max_length=50, verbose_name='Service Type')),
                ('txn_detail', models.JSONField(verbose_name='Transaction JSON')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('userAccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Linked User')),
            ],
        ),
    ]
