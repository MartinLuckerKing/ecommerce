# Generated by Django 4.0.4 on 2022-10-18 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_remove_cartitem_user'),
        ('order', '0005_alter_orderproduct_order_alter_orderproduct_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='quantity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.cartitem'),
        ),
    ]