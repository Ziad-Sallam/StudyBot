# Generated by Django 5.1.4 on 2024-12-24 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_userassignment_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='description',
            field=models.TextField(default='No description'),
        ),
    ]
