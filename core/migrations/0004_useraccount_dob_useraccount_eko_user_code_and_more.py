# Generated by Django 4.2.5 on 2023-12-10 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_useraccount_pancard_no"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="dob",
            field=models.DateField(blank=True, null=True, verbose_name="Date of Birth"),
        ),
        migrations.AddField(
            model_name="useraccount",
            name="eko_user_code",
            field=models.CharField(
                blank=True, max_length=500, null=True, verbose_name="Eko User Code"
            ),
        ),
        migrations.AddField(
            model_name="useraccount",
            name="platform_id",
            field=models.CharField(
                blank=True, max_length=500, null=True, verbose_name="Platform id"
            ),
        ),
        migrations.AddField(
            model_name="useraccount",
            name="userManager",
            field=models.CharField(
                blank=True, max_length=120, null=True, verbose_name="User Manager"
            ),
        ),
    ]
