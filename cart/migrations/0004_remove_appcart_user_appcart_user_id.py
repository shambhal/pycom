# Generated by Django 4.2 on 2023-12-16 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_appcart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appcart',
            name='user',
        ),
        migrations.AddField(
            model_name='appcart',
            name='user_id',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
