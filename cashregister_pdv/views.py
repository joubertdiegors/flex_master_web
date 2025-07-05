from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.timezone import now
from django.conf import settings
from .models import CashRegister, FavoriteProduct, PdvSale, PdvSaleItem, PdvSalePayment, PdvHoldSale, PdvHoldSaleItem
from products.models import Product
from .forms import FavoriteProductForm
import json
import uuid
from datetime import timezone


# PDV Abertura/Fechamento de caixa
@csrf_exempt
def get_open_cash_status(request):
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    branch_id = request.GET.get("branch_id")
    terminal = request.GET.get("terminal")

    try:
        cash = CashRegister.objects.get(
            branch_id=branch_id,
            terminal_number=terminal,
            closed_at__isnull=True
        )

        return JsonResponse({
            "status": "open",
            "cash_register": {
                "id": str(cash.id),
                "opened_at": cash.opened_at,
                "operator_id": cash.operator_id,
                "opening_amount": float(cash.opening_amount)
            }
        })

    except CashRegister.DoesNotExist:
        return JsonResponse({"status": "closed"})

@csrf_exempt
def list_cash_registers(request):
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    cash_list = CashRegister.objects.all().order_by("opened_at")

    result = []
    for cash in cash_list:
        result.append({
            "id": str(cash.id),
            "branch_id": cash.branch_id,
            "terminal_number": cash.terminal_number,
            "operator_id": cash.operator_id,
            "opened_at": cash.opened_at,
            "opening_amount": float(cash.opening_amount),
            "closed_at": cash.closed_at,
            "closing_amount": float(cash.closing_amount) if cash.closing_amount is not None else None,
        })

    return JsonResponse(result, safe=False)

@csrf_exempt
def pdv_open_cash(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")

    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    try:
        data = json.loads(request.body)

        cash = CashRegister.objects.create(
            id=uuid.UUID(data["id"]),
            branch_id=data["branch_id"],
            terminal_number=data["terminal_number"],
            operator_id=data["operator_id"],
            opened_at=now(),
            opening_amount=data["opening_amount"]
        )

        return JsonResponse({"status": "ok", "id": str(cash.id)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def pdv_close_cash(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método inválido")

    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    try:
        data = json.loads(request.body)
        print("Recebido:", data)
        cash = CashRegister.objects.get(id=uuid.UUID(data["id"]))

        cash.closed_at = now()
        cash.closing_amount = data["closing_amount"]
        cash.total_sales = data["total_sales"]
        cash.total_cash = data["total_cash"]
        cash.total_machine = data["total_machine"]
        cash.total_credit = data["total_credit"]
        cash.notes = data.get("notes", "")
        cash.save()

        return JsonResponse({"status": "ok"})

    except CashRegister.DoesNotExist:
        return JsonResponse({"error": "Registro de caixa não encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def pdv_cash_history(request):
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    cash_registers = CashRegister.objects.all().order_by("-opened_at")

    data = []
    for cash in cash_registers:
        data.append({
            "id": str(cash.id),
            "branch_id": cash.branch_id,
            "terminal_number": cash.terminal_number,
            "operator_id": cash.operator_id,
            "opened_at": cash.opened_at.isoformat() if cash.opened_at else None,
            "closed_at": cash.closed_at.isoformat() if cash.closed_at else None,
            "opening_amount": float(cash.opening_amount),
            "closing_amount": float(cash.closing_amount) if cash.closing_amount else None,
            "total_sales": float(cash.total_sales),
            "total_cash": float(cash.total_cash),
            "total_machine": float(cash.total_machine),
            "total_credit": float(cash.total_credit),
            "notes": cash.notes,
            "status": "open" if cash.closed_at is None else "closed"
        })

    return JsonResponse({"cash_registers": data})


class CashRegisterHistoryView(View):
    template_name = 'cashregister_history.html'

    def get(self, request, *args, **kwargs):
        cash_registers = CashRegister.objects.select_related('operator').order_by('-opened_at')
        context = {
            'cash_registers': cash_registers
        }
        return render(request, self.template_name, context)

# Produtos Favoritos PDV
class FavoriteProductListView(LoginRequiredMixin, ListView):
    model = FavoriteProduct
    template_name = 'favorite_list.html'
    context_object_name = 'favorites'
    ordering = ['order']

class FavoriteProductCreateView(LoginRequiredMixin, CreateView):
    model = FavoriteProduct
    form_class = FavoriteProductForm
    template_name = 'favorite_form.html'
    success_url = reverse_lazy('favorite_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class FavoriteProductDetailView(LoginRequiredMixin, DetailView):
    model = FavoriteProduct
    template_name = 'favorite_detail.html'
    context_object_name = 'favorite'

class FavoriteProductUpdateView(LoginRequiredMixin, UpdateView):
    model = FavoriteProduct
    form_class = FavoriteProductForm
    template_name = 'favorite_form.html'
    success_url = reverse_lazy('favorite_list')

class FavoriteProductDeleteView(LoginRequiredMixin, DeleteView):
    model = FavoriteProduct
    template_name = 'favorite_confirm_delete.html'
    success_url = reverse_lazy('favorite_list')


# Tela de tickets de vendas pelo PDV
class PdvSaleListView(ListView):
    model = PdvSale
    template_name = "pdvsale_list.html"
    context_object_name = "sales"

    def get_queryset(self):
        return (
            PdvSale.objects
            .select_related("cash_register", "customer")
            .prefetch_related("payments__payment_method")
            .order_by("-created_at")
        )
    
class PdvSaleDetailView(DetailView):
    model = PdvSale
    template_name = "pdvsale_detail.html"
    context_object_name = "sale"

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("cash_register__operator", "customer")
            .prefetch_related("items__product", "payments__payment_method")
        )


# API
def pdv_favorite_list(request):
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    favorites = FavoriteProduct.objects.select_related("product").order_by("order")

    result = [
        {
            "product_id": fav.product.id,
            "name": fav.product.name,
            "color": fav.color,
            "order": fav.order,
        }
        for fav in favorites
    ]

    return JsonResponse({"favorites": result})

# API Vendas do PDV
@csrf_exempt
def pdv_sales_list(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Método não permitido")

    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    cash_register_id = request.GET.get("cash_register_id")
    date_str = request.GET.get("date")
    ticket_number = request.GET.get("ticket_number")

    queryset = PdvSale.objects.all()

    if cash_register_id:
        queryset = queryset.filter(cash_register_id=cash_register_id)

    if ticket_number:
        queryset = queryset.filter(ticket_number=ticket_number)

    if date_str:
        date_obj = parse_date(date_str)
        if date_obj:
            queryset = queryset.filter(created_at__date=date_obj)

    data = []
    for sale in queryset.order_by("-created_at")[:3000]:  # limita a 3000 vendas recentes
        items = [
            {
                "product_id": item.product_id,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "discount": float(item.discount),
                "line_total": float(item.line_total),
                "observation": item.observation
            }
            for item in sale.items.all()
        ]

        data.append({
            "id": str(sale.id),
            "ticket_number": sale.ticket_number,
            "customer_id": sale.customer_id,
            "cash_register_id": sale.cash_register_id,
            "total_amount": float(sale.total_amount),
            "total_discount": float(sale.total_discount),
            "amount_paid": float(sale.amount_paid),
            "change_given": float(sale.change_given),
            "created_at": sale.created_at.isoformat(),
            "items": items,
            "payments": [
                {
                    "payment_method_id": p.payment_method_id,
                    "amount": float(p.amount)
                } for p in sale.payments.all()
            ]
        })

    return JsonResponse({"sales": data})

@csrf_exempt
def pdv_sale_create(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método não permitido")

    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    try:
        data = json.loads(request.body)

        sale = PdvSale.objects.create(
            id=uuid.UUID(data["id"]),
            cash_register_id=data["cash_register_id"],
            ticket_number=data["ticket_number"],
            customer_id=data.get("customer_id"),
            total_amount=data["total_amount"],
            total_discount=data["total_discount"],
            amount_paid=data["amount_paid"],
            change_given=data.get("change_given", 0),
            created_at=data.get("created_at") or timezone.now()
        )

        for item in data["items"]:
            PdvSaleItem.objects.create(
                sale=sale,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                discount=item["discount"],
                line_total=item["line_total"],
                observation=item.get("observation", "")
            )

        for payment in data.get("payments", []):
            PdvSalePayment.objects.create(
                sale=sale,
                payment_method_id=payment["payment_method_id"],
                amount=payment["amount"]
            )

        return JsonResponse({"status": "ok", "sale_id": str(sale.id)})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

# Compras em Espera do PDV
@csrf_exempt
def pdv_hold_create(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Método não permitido")
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    try:
        data = json.loads(request.body)

        hold = PdvHoldSale.objects.create(
            id=uuid.UUID(data["id"]),
            identifier=data["identifier"],
            cash_register_id=data["cash_register_id"],
            customer_id=data.get("customer_id"),
            note=data.get("note", "")
        )

        for item in data["items"]:
            PdvHoldSaleItem.objects.create(
                id=uuid.UUID(item["id"]),
                hold_sale=hold,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                discount=item["discount"],
                line_total=item["line_total"],
                observation=item.get("observation", "")
            )

        return JsonResponse({"status": "ok", "hold_id": str(hold.id)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    
@csrf_exempt
def pdv_hold_list(request):
    if request.method != "GET":
        return HttpResponseBadRequest("Método não permitido")
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    data = []
    for hold in PdvHoldSale.objects.order_by("-created_at"):
        items = [
            {
                "product_id": item.product_id,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "discount": float(item.discount),
                "line_total": float(item.line_total),
                "observation": item.observation
            }
            for item in hold.items.all()
        ]

        data.append({
            "id": str(hold.id),
            "identifier": hold.identifier,
            "customer_id": hold.customer_id,
            "note": hold.note,
            "created_at": hold.created_at.isoformat(),
            "cash_register_id": hold.cash_register_id,
            "items": items
        })

    return JsonResponse({"holds": data})

@csrf_exempt
def pdv_hold_delete(request, hold_id):
    if request.method != "DELETE":
        return HttpResponseBadRequest("Método não permitido")
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    try:
        hold = PdvHoldSale.objects.get(id=hold_id)
        hold.delete()
        return JsonResponse({"status": "deleted"})
    except PdvHoldSale.DoesNotExist:
        return JsonResponse({"error": "Espera não encontrada"}, status=404)

