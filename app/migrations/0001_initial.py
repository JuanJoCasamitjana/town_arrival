# Generated by Django 4.2.6 on 2023-11-18 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_alter_profile_rol'),
    ]

    operations = [
        migrations.CreateModel(
            name='Casa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.TextField(max_length=150)),
                ('descripcion', models.TextField(max_length=500)),
                ('imagen', models.ImageField(upload_to='')),
                ('localidad', models.TextField(max_length=50)),
                ('direccion', models.TextField(max_length=100)),
                ('arrendador', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]
