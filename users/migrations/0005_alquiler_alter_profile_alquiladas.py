# Generated by Django 4.2.6 on 2023-11-30 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_casa_arrendador"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0004_profile_alquiladas"),
    ]

    operations = [
        migrations.CreateModel(
            name="Alquiler",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("FechaInicio", models.DateTimeField()),
                ("FechaFinal", models.DateTimeField()),
                (
                    "alquilo",
                    models.OneToOneField(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.casa",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="profile",
            name="alquiladas",
            field=models.ManyToManyField(blank=True, to="users.alquiler"),
        ),
    ]
