# Generated by Django 4.2 on 2024-02-07 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_rename_customer_id_order_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='order_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order'),
        ),
    ]
