# Generated by Django 2.1.5 on 2019-12-10 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_auto_20191209_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='desc',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='imageSrc',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='data',
            name='microReview',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='tags',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
