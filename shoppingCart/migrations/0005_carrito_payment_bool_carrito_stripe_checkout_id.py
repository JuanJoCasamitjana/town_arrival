# Generated by Django 4.2.6 on 2023-12-07 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shoppingCart", "0004_remove_carrito_payment_bool_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="carrito",
            name="payment_bool",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="carrito",
            name="stripe_checkout_id",
            field=models.CharField(default="", max_length=500),
        ),
    ]
