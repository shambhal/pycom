# Generated by Django 4.2 on 2023-12-21 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxes', '0004_alter_tax_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name': 'Tax', 'verbose_name_plural': 'Taxes'},
        ),
    ]
