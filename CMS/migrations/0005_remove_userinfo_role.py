# Generated by Django 2.1.7 on 2019-10-20 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0004_auto_20191020_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='role',
        ),
    ]
