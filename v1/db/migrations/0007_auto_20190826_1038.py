# Generated by Django 2.2.4 on 2019-08-26 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_auto_20190814_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='landingpagedb',
            options={'ordering': ('-registered_date',)},
        ),
        migrations.AddField(
            model_name='landingpagedb',
            name='stay_time',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
