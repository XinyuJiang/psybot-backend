# Generated by Django 2.1.5 on 2019-03-31 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psybot', '0006_auto_20190320_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotioninfo',
            name='create_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
