# Generated by Django 2.1.3 on 2018-11-29 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20181129_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='rate',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
