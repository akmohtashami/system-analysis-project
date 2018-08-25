# Generated by Django 2.0.5 on 2018-06-15 22:36

from django.db import migrations
import proxypay.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180615_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=proxypay.fields.EnumField(default='Customer', enum=users.models.UserType, max_length=8, verbose_name='type'),
        ),
    ]
