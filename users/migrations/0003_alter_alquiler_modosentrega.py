# Generated by Django 4.2.6 on 2023-12-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_alquiler_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alquiler',
            name='modosEntrega',
            field=models.CharField(choices=[('LB', 'Dejar las llaves en buzón'), ('LV', 'Dejar las llaves con vecino'), ('LP', 'Entrega de llaves personal')], default='LP', max_length=2),
        ),
    ]