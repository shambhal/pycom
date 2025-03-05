# Generated by Django 4.2 on 2024-03-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0019_book_extra_info_bookhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookhistory',
            name='info',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='status',
            field=models.CharField(choices=[('UN', 'UNAVAILABLE'), ('AV', 'AVAILABLE'), ('CAN', 'CANCELLED'), ('BOOKED', 'BOOKED'), ('REFUNDED', 'REFUNDED')], default='AV', max_length=15),
        ),
    ]
