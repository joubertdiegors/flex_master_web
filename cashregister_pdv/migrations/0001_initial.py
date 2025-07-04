# Generated by Django 4.2.13 on 2025-05-12 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payment_methods', '0001_initial'),
        ('branches', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashRegister',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('terminal_number', models.CharField(max_length=10)),
                ('opened_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('opening_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('closing_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_sales', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_cash', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_machine', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_credit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='branches.branch')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-opened_at'],
            },
        ),
        migrations.CreateModel(
            name='CashRegisterPayment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cash_register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='cashregister_pdv.cashregister')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='payment_methods.paymentmethod')),
            ],
        ),
    ]
