# Generated by Django 4.2.2 on 2023-06-26 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0002_alter_medicine_med_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='med_username',
            field=models.TextField(default='medicine', unique=True),
        ),
    ]