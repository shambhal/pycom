# Generated by Django 4.2 on 2023-12-21 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0011_alter_sspecial_options_alter_book_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='order',
        ),
        migrations.AlterField(
            model_name='book',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.service'),
        ),
    ]
