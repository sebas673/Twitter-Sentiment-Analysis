# Generated by Django 2.2.6 on 2019-10-30 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='keyword',
            field=models.CharField(default=models.CharField(max_length=100), max_length=50),
        ),
    ]
