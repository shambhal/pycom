# Generated by Django 4.2 on 2023-12-25 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0017_book_order_item_id_bookhistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookhistory',
            name='book',
        ),
        migrations.RemoveConstraint(
            model_name='book',
            name='unique_booking',
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('dated', 'service', 'slot', 'status'), name='unique2_booking'),
        ),
        migrations.DeleteModel(
            name='BookHistory',
        ),
    ]
