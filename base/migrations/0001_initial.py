# Generated by Django 4.2.8 on 2024-04-05 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='ip_address')),
            ],
        ),
        migrations.CreateModel(
            name='PagePic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_pic', models.ImageField(upload_to='images', verbose_name='website_pic')),
            ],
            options={
                'verbose_name': 'website_pic',
                'verbose_name_plural': 'website_pic',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Category-title')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Category-Addres')),
                ('status', models.BooleanField(default=True, verbose_name='Make it publish')),
                ('position', models.IntegerField(verbose_name='position')),
            ],
        ),
        migrations.CreateModel(
            name='ProductHit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TheProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=50, verbose_name='product')),
                ('price', models.IntegerField(default=50, verbose_name='price')),
                ('pic_sample', models.ImageField(upload_to='images', verbose_name='picture')),
                ('description', models.TextField(verbose_name='description')),
                ('period', models.CharField(choices=[('1', 'One_months'), ('3', 'Three_months'), ('6', 'Six_months')], default='1', max_length=1, verbose_name='period')),
                ('max_users', models.CharField(choices=[('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'), ('5', 'Five')], default='1', max_length=1, verbose_name='Users_in_same_time')),
                ('imported_at', models.DateTimeField(auto_now_add=True, verbose_name='imported_at')),
                ('availability', models.CharField(choices=[('A', 'Available'), ('U', 'Unavailable'), ('I', 'Investigate'), ('B', 'Banned')], default='I', max_length=1, verbose_name='Status')),
                ('category', models.ManyToManyField(related_name='category', to='base.productcategory', verbose_name='Category')),
            ],
        ),
    ]
