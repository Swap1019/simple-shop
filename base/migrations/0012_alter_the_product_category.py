# Generated by Django 4.2.5 on 2023-10-02 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_product_category_the_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='the_product',
            name='category',
            field=models.ManyToManyField(related_name='category', to='base.product_category', verbose_name='Category'),
        ),
    ]
