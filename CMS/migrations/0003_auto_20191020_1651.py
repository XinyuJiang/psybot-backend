# Generated by Django 2.1.7 on 2019-10-20 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0002_auto_20191020_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginfo',
            name='contentid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='loginfo',
            name='label',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='loginfo',
            name='text',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]