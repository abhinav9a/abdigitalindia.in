# Generated by Django 4.2.5 on 2023-12-10 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0004_useraccount_dob_useraccount_eko_user_code_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="useraccount",
            name="fullName",
        ),
        migrations.AlterField(
            model_name="useraccount",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="First Name"
            ),
        ),
        migrations.AlterField(
            model_name="useraccount",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Last Name"
            ),
        ),
    ]
