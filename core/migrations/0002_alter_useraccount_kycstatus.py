# Generated by Django 4.2.3 on 2023-11-27 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='kycStatus',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('R', 'Rejected')], default='P', max_length=20),
        ),
    ]
