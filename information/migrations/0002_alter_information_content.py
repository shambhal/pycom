# Generated by Django 4.2 on 2024-04-29 10:22

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
