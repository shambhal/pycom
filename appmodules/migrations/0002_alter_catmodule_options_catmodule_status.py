# Generated by Django 4.2 on 2024-05-13 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmodules', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catmodule',
            options={'verbose_name': 'Category Banner'},
        ),
        migrations.AddField(
            model_name='catmodule',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
