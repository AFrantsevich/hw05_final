# Generated by Django 2.2.6 on 2022-09-08 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_whovoted_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whovoted',
            name='post_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='whovoted',
            name='type',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='whovoted',
            name='username',
            field=models.TextField(null=True),
        ),
    ]