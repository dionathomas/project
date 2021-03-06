# Generated by Django 3.0.5 on 2020-04-18 04:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200417_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='tutorial_imageurl',
            field=models.CharField(default='static/main/images/.jpg', max_length=200),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='tutorial_link',
            field=models.CharField(blank=True, default='https://en.wikipedia.org/wiki/', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_title',
            field=models.CharField(default='Company Name', max_length=200),
        ),
    ]
