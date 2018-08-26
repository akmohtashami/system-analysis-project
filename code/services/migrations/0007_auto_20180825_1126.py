# Generated by Django 2.0.8 on 2018-08-25 11:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import proxypay.fields
import services.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0006_auto_20180819_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerequest',
            name='currency',
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='link',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='operator',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='operator'),
        ),
        migrations.AlterField(
            model_name='servicerequest',
            name='status',
            field=proxypay.fields.EnumField(default='PENDING', enum=services.models.RequestStatus, max_length=10, verbose_name='status'),
        ),
    ]