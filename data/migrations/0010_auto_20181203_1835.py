# Generated by Django 2.1.3 on 2018-12-03 18:35

import data.models
from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_auto_20181203_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=data.models.post_image_path),
        ),
    ]
