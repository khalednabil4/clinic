# Generated by Django 3.2.18 on 2024-12-02 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0003_rename_service_patientcondition_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='IsActive',
            field=models.BooleanField(default=True),
        ),
    ]