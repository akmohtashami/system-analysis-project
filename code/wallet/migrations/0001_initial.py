# Generated by Django 2.0.5 on 2018-06-15 21:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import wallet.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', enumfields.fields.EnumField(enum=wallet.models.Currency, max_length=10, verbose_name='currency')),
                ('credit', models.FloatField(default=0, verbose_name='credit')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='owner')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='wallet',
            unique_together={('currency', 'owner')},
        ),
    ]