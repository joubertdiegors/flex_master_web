# Generated by Django 4.2.13 on 2025-01-14 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]