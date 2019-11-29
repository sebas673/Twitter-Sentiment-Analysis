# Generated by Django 2.2.6 on 2019-11-28 22:12

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0027_auto_20191128_0614'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='old_id_list',
            field=models.CharField(blank=True, max_length=200, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]