# Generated by Django 4.2.2 on 2023-06-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prescription', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='med_name',
            field=models.TextField(),
        ),
    ]