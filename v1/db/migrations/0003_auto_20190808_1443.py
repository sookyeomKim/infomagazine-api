# Generated by Django 2.2.4 on 2019-08-08 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20190808_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpagedb',
            name='registered_date',
            field=models.CharField(max_length=13),
        ),
    ]
