# Generated by Django 4.2.6 on 2023-11-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rol',
            field=models.CharField(choices=[('Ar', 'Arrendador'), ('Cl', 'Cliente')], max_length=2),
        ),
    ]
