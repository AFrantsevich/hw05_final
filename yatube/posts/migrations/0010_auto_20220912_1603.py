# Generated by Django 2.2.6 on 2022-09-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20220908_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='raiting',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Raiting',
        ),
    ]
