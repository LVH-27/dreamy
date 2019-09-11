# Generated by Django 2.2.5 on 2019-09-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreamy', '0005_auto_20190911_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='/static/dreamy/images/default_avatar.png', null=True, upload_to='avatars/'),
        ),
    ]
