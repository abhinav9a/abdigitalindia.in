# Generated by Django 4.2.7 on 2024-03-16 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0065_cmstxncallbackbyeko'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='client_ref_id',
        ),
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='commission',
        ),
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='tid',
        ),
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='tx_status',
        ),
        migrations.RemoveField(
            model_name='cmstxncallbackbyeko',
            name='userAccount',
        ),
    ]
