# Generated by Django 4.2.5 on 2023-11-26 11:39

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="kycinformation",
            name="documentFile",
        ),
        migrations.AddField(
            model_name="kycinformation",
            name="documentFile1",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=backend.models.document_file_path,
                verbose_name="Document File1",
            ),
        ),
        migrations.AddField(
            model_name="kycinformation",
            name="documentFile2",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=backend.models.document_file_path,
                verbose_name="Document File2",
            ),
        ),
    ]
