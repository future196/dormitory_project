# Generated by Django 2.1.1 on 2018-12-27 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_repair_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair',
            name='wait',
            field=models.CharField(default='', max_length=20),
        ),
    ]
