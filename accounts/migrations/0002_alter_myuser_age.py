# Generated by Django 4.2.2 on 2023-06-13 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='age',
            field=models.IntegerField(blank=True),
        ),
    ]