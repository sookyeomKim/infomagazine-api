# Generated by Django 2.2.1 on 2019-05-21 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_name', models.CharField(max_length=100)),
                ('corp_sub_name', models.CharField(blank=True, max_length=100)),
                ('corp_header', models.CharField(blank=True, max_length=20)),
                ('corp_address', models.CharField(blank=True, max_length=200)),
                ('corp_num', models.CharField(blank=True, max_length=50, unique=True)),
                ('corp_desc', models.CharField(blank=True, max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'company',
            },
        ),
    ]
