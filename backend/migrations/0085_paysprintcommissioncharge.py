# Generated by Django 4.2.10 on 2024-09-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0084_wallet2_alter_paysprintaepstxndetail_ack_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaySprintCommissionCharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100, unique=True)),
                ('charge', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
