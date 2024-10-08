# Generated by Django 4.2.7 on 2024-05-10 04:32

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0078_otherservices_address_otherservices_adhaar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherservices',
            name='doc1',
            field=models.FileField(blank=True, upload_to=backend.models.other_service_file_path, verbose_name='Supporting Document 1'),
        ),
        migrations.AlterField(
            model_name='otherservices',
            name='doc2',
            field=models.FileField(blank=True, upload_to=backend.models.other_service_file_path, verbose_name='Supporting Document 2'),
        ),
        migrations.AlterField(
            model_name='otherservices',
            name='doc3',
            field=models.FileField(blank=True, upload_to=backend.models.other_service_file_path, verbose_name='Supporting Document 3'),
        ),
        migrations.AlterField(
            model_name='otherservices',
            name='doc4',
            field=models.FileField(blank=True, upload_to=backend.models.other_service_file_path, verbose_name='Supporting Document 4'),
        ),
    ]
