# Generated by Django 4.2.13 on 2025-01-11 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_stock_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock_quantity',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=10),
        ),
    ]