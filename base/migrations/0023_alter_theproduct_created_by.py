# Generated by Django 4.2.5 on 2023-11-24 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0022_remove_theproduct_product_shop_delete_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theproduct',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='user_id'),
        ),
    ]
