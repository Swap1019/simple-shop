# Generated by Django 4.2.5 on 2023-11-19 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0019_theproduct_product_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(default=None, max_length=50, verbose_name='Shop name'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='owner',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id', verbose_name='Shop owner'),
        ),
    ]
