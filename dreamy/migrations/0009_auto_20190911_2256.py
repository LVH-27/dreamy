# Generated by Django 2.2.5 on 2019-09-11 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dreamy', '0008_auto_20190911_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
