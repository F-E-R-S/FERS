# Generated by Django 3.1.7 on 2021-05-18 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_sign_avg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sign',
            name='avg',
            field=models.FloatField(default=0.0),
        ),
    ]
