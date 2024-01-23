# Generated by Django 4.2.4 on 2023-10-10 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital_management_app", "0009_alter_customuser_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email address"
            ),
        ),
    ]