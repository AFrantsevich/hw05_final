# Generated by Django 2.2.16 on 2022-10-14 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WhoVoted',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='create',
            new_name='created',
        ),
    ]
