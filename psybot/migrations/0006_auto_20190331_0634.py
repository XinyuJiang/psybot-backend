# Generated by Django 2.1.7 on 2019-03-31 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psybot', '0005_auto_20190320_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotioninfo',
            name='create_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
