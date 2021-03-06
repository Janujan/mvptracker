# Generated by Django 2.1.4 on 2018-12-25 07:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0002_auto_20181225_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='image_url',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 25, 7, 6, 59, 327121, tzinfo=utc)),
        ),
    ]
