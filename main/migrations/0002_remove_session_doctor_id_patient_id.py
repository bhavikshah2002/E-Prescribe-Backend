# Generated by Django 4.2.2 on 2023-06-20 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='session',
            name='doctor_id&patient_id',
        ),
    ]
