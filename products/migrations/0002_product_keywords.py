# Generated by Django 4.2.13 on 2025-01-09 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='keywords',
            field=models.TextField(blank=True, help_text='Palavras-chave separadas por vírgulas para busca.', null=True),
        ),
    ]
