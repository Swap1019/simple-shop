# Generated by Django 4.2.5 on 2023-11-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersellerinfo',
            name='user_id',
            field=models.UUIDField(default=None),
        ),
    ]
