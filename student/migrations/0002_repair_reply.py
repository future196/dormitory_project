# Generated by Django 2.1.1 on 2018-12-27 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair',
            name='reply',
            field=models.CharField(default='', max_length=200),
        ),
    ]
