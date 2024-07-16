# Generated by Django 4.2.11 on 2024-07-15 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_alter_cartsshippingstatus_progress_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='progress_status',
            field=models.CharField(choices=[('0', 'Refuesed'), ('25', 'In process'), ('50', 'Preparation to ship'), ('75', 'In shipping progress'), ('100', 'Shipped')], default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CartsShippingStatus',
        ),
    ]