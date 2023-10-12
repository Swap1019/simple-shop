# Generated by Django 4.2.5 on 2023-10-11 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_theproduct_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='ip_address')),
            ],
        ),
        migrations.CreateModel(
            name='ProductHit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.ipaddress')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.theproduct')),
            ],
        ),
        migrations.AddField(
            model_name='theproduct',
            name='hits',
            field=models.ManyToManyField(blank=True, related_name='hits', through='base.ProductHit', to='base.ipaddress', verbose_name='view_counts'),
        ),
    ]
