# Generated by Django 2.2.5 on 2019-09-08 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreamy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
