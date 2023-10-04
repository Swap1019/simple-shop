# Generated by Django 4.2.5 on 2023-10-01 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_the_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='product_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Category-title')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Category-Addres')),
                ('status', models.BooleanField(default=True, verbose_name='Make it publish')),
                ('position', models.IntegerField(verbose_name='position')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='base.product_category', verbose_name='parent')),
            ],
        ),
        migrations.AddField(
            model_name='the_product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='base.product_category', verbose_name='Category'),
        ),
    ]
