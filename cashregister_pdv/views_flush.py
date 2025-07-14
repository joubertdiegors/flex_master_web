from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import transaction
from .models import (
    CashRegister,
    CashRegisterPayment,
    FavoriteProduct,
    PdvSale,
    PdvSaleItem,
    PdvSalePayment,
    PdvHoldSale,
    PdvHoldSaleItem,
)

@csrf_exempt  # pode ser removido se quiser usar proteção CSRF do Django
def flush_pdv_data(request):
    if request.method == "GET":
        return render(request, "confirm_flush.html")

    elif request.method == "POST":
        with transaction.atomic():
            PdvSaleItem.objects.all().delete()
            PdvSalePayment.objects.all().delete()
            PdvSale.objects.all().delete()
            PdvHoldSaleItem.objects.all().delete()
            PdvHoldSale.objects.all().delete()
            CashRegisterPayment.objects.all().delete()
            CashRegister.objects.all().delete()
            FavoriteProduct.objects.all().delete()

        return render(request, "flush_done.html")
