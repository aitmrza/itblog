# Generated by Django 3.0.6 on 2020-06-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20200618_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'статья', 'verbose_name_plural': 'статьи'},
        ),
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'автор', 'verbose_name_plural': 'авторы'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'комментарий', 'verbose_name_plural': 'комментарии'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тег', 'verbose_name_plural': 'теги'},
        ),
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='articles/20200620'),
        ),
    ]