# Generated by Django 2.2.6 on 2019-11-28 03:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0024_auto_20191128_0346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='negIDs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=70), null=True, size=None),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='posIDs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=70), null=True, size=None),
        ),
    ]