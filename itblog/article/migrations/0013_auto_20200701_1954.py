# Generated by Django 3.0.6 on 2020-07-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20200624_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='articles/20200701'),
        ),
    ]
