# Generated by Django 4.2.4 on 2023-09-27 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytimeslots',
            name='time_slots',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
