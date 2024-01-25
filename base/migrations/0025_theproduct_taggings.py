# Generated by Django 4.2.8 on 2024-01-25 18:15

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('base', '0024_alter_theproduct_availability_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='theproduct',
            name='taggings',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]