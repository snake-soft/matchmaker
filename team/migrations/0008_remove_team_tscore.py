# Generated by Django 2.0.8 on 2018-08-16 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_auto_20180815_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='tscore',
        ),
    ]