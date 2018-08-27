# Generated by Django 2.0.4 on 2018-08-26 18:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9\\_\\-]+$')], verbose_name='short name')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('is_visible', models.BooleanField(default=True, help_text='Designate whether this type of requests can be created.', verbose_name='visible')),
                ('text', models.TextField(blank=True, verbose_name='text')),
            ],
        ),
    ]