# Generated by Django 4.2.7 on 2023-12-25 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0019_alter_aepstxncallbackbyeko_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aepstxncallbackbyeko',
            name='tx_status',
            field=models.CharField(choices=[('P', 'Pending'), ('S', 'Success'), ('C', 'Cancel')], max_length=20),
        ),
    ]
