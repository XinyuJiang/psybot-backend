# Generated by Django 2.1.7 on 2019-10-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='portrait',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]