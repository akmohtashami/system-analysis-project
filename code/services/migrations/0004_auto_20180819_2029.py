# Generated by Django 2.0.8 on 2018-08-19 20:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20180819_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetype',
            name='short_name',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9\\_\\-]+$')], verbose_name='short name'),
        ),
    ]
