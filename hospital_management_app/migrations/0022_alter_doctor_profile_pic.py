# Generated by Django 4.2.7 on 2023-11-13 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hospital_management_app", "0021_merge_20231106_1000"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="profile_pic",
            field=models.FileField(null=True, upload_to="avatars/"),
        ),
    ]
