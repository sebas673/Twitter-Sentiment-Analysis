# Generated by Django 2.2.6 on 2019-11-20 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0014_auto_20191112_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='most_favorited',
            field=models.IntegerField(default=0),
        ),
    ]
