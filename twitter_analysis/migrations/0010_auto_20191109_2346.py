# Generated by Django 2.2.6 on 2019-11-09 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0009_merge_20191103_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='negID1',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='campaign',
            name='negID2',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='campaign',
            name='posID1',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='campaign',
            name='posID2',
            field=models.CharField(default='', max_length=100),
        ),
    ]
