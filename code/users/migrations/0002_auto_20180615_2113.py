# Generated by Django 2.0.5 on 2018-06-15 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='monthly_salary',
            field=models.PositiveIntegerField(default=0, verbose_name='monthly salary'),
        ),
    ]
