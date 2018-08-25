# Generated by Django 2.0.8 on 2018-08-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20180825_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicetype',
            name='max_amount',
            field=models.FloatField(default=None, null=True, verbose_name='max amount'),
        ),
        migrations.AddField(
            model_name='servicetype',
            name='min_amount',
            field=models.FloatField(default=None, null=True, verbose_name='min amount'),
        ),
    ]
