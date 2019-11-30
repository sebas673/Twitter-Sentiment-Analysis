# Generated by Django 2.2.6 on 2019-11-30 20:33

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0030_auto_20191130_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='old_id_list',
            field=models.CharField(blank=True, max_length=400, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
