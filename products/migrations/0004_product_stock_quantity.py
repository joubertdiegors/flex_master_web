# Generated by Django 4.2.13 on 2025-01-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_quantity',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
