# Generated by Django 4.2.10 on 2024-10-11 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0089_alter_paysprintaepstxndetail_aadhaar_no_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet2',
            name='is_hold',
        ),
        migrations.AddField(
            model_name='wallet2',
            name='held_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
