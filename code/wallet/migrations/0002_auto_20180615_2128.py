# Generated by Django 2.0.5 on 2018-06-15 21:28

from django.db import migrations
import proxypay.fields
import wallet.models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='currency',
            field=proxypay.fields.EnumField(enum=wallet.models.Currency, max_length=3, verbose_name='currency'),
        ),
    ]
