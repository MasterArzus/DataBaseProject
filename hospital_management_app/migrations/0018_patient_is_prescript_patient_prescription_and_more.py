# Generated by Django 4.2.6 on 2023-11-04 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_management_app', '0017_alter_doctor_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='is_prescript',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='prescription',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='profile_pic',
            field=models.FileField(null=True, upload_to='avatars'),
        ),
    ]
