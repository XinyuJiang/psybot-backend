# Generated by Django 2.1.5 on 2019-03-06 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psybot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activityinfo',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='password',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='openid',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]