# Generated by Django 4.2.5 on 2023-09-23 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_page_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='the_product',
            name='max_users',
        ),
        migrations.RemoveField(
            model_name='the_product',
            name='period',
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.ForeignKey(max_length=1, on_delete=django.db.models.deletion.CASCADE, related_name='period', to='base.the_product', verbose_name='period')),
                ('user_amount', models.ForeignKey(max_length=1, on_delete=django.db.models.deletion.CASCADE, related_name='max_users', to='base.the_product', verbose_name='max_users')),
            ],
        ),
    ]