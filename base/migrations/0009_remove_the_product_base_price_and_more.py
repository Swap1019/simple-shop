# Generated by Django 4.2.5 on 2023-09-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_the_product_time_limit_prices_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='the_product',
            name='base_price',
        ),
        migrations.RemoveField(
            model_name='the_product',
            name='time',
        ),
        migrations.RemoveField(
            model_name='the_product',
            name='time_limit_prices',
        ),
        migrations.RemoveField(
            model_name='the_product',
            name='users_amount',
        ),
        migrations.RemoveField(
            model_name='the_product',
            name='users_amount_prices',
        ),
        migrations.AddField(
            model_name='the_product',
            name='max_users',
            field=models.CharField(choices=[('1', 'one'), ('2', 'two'), ('3', 'three'), ('4', 'four'), ('5', 'five')], default='1', max_length=1, verbose_name='Users_in_same_time'),
        ),
        migrations.AddField(
            model_name='the_product',
            name='period',
            field=models.CharField(choices=[('1', 'one_months'), ('3', 'three_months'), ('6', 'six_months')], default='1', max_length=1, verbose_name='period'),
        ),
        migrations.AddField(
            model_name='the_product',
            name='price',
            field=models.IntegerField(default=50, max_length=60, verbose_name='price'),
        ),
        migrations.DeleteModel(
            name='time_amount',
        ),
        migrations.DeleteModel(
            name='user_amount',
        ),
    ]