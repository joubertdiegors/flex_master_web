# Generated by Django 4.2.13 on 2025-05-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_cash', models.BooleanField(default=False)),
                ('is_credit', models.BooleanField(default=False)),
                ('is_machine_payment', models.BooleanField(default=False)),
                ('show_on_site', models.BooleanField(default=False)),
                ('show_on_pdv', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
