# Generated by Django 4.2.6 on 2023-12-09 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_categoria_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='url',
            field=models.SlugField(unique=True),
        ),
    ]
