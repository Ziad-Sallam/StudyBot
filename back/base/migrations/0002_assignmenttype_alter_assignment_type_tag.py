# Generated by Django 5.1.1 on 2024-11-06 00:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='assignment',
            name='type_tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.assignmenttype'),
        ),
    ]
