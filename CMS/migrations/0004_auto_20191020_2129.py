# Generated by Django 2.1.7 on 2019-10-20 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMS', '0003_auto_20191020_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginfo',
            old_name='label',
            new_name='action',
        ),
        migrations.RemoveField(
            model_name='loginfo',
            name='text',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='role',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
