# Generated by Django 3.1.7 on 2021-05-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20210518_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='sign',
            name='higher_than_50',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sign',
            name='lower_than_50',
            field=models.IntegerField(default=0),
        ),
    ]
