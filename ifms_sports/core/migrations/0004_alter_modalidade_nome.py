# Generated by Django 5.1.1 on 2024-09-20 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_modalidade_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modalidade',
            name='nome',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
