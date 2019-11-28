# Generated by Django 2.2.6 on 2019-11-28 06:10

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0025_auto_20191128_0349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='id_list',
            field=models.CharField(blank=True, max_length=100, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Tweet IDs'),
        ),
    ]
