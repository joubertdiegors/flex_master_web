from django.db import models

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_cash = models.BooleanField(default=False)
    is_credit = models.BooleanField(default=False)
    is_machine_payment = models.BooleanField(default=False)

    show_on_site = models.BooleanField(default=False)
    show_on_pdv = models.BooleanField(default=True)

    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
