from django.conf import settings
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden

from .models import PaymentMethod
from cashregister_pdv.models import CashRegister, CashRegisterPayment

from app.mixins.mixins import StaffRequiredMixin, AdminRequiredMixin


class PaymentMethodListView(StaffRequiredMixin, ListView):
    model = PaymentMethod
    template_name = "paymentmethod_list.html"
    context_object_name = "methods"


class PaymentMethodCreateView(StaffRequiredMixin, CreateView):
    model = PaymentMethod
    fields = ["name", "is_active", "is_cash", "is_credit", "is_machine_payment", "show_on_site", "show_on_pdv", "order"]
    template_name = "paymentmethod_form.html"
    success_url = reverse_lazy("payment_method_list")


class PaymentMethodDetailView(StaffRequiredMixin, DetailView):
    model = PaymentMethod
    template_name = "paymentmethod_detail.html"
    context_object_name = "method"


class PaymentMethodUpdateView(StaffRequiredMixin, UpdateView):
    model = PaymentMethod
    fields = ["name", "is_active", "is_cash", "is_credit", "is_machine_payment", "show_on_site", "show_on_pdv", "order"]
    template_name = "paymentmethod_form.html"
    success_url = reverse_lazy("payment_method_list")


class PaymentMethodDeleteView(AdminRequiredMixin, DeleteView):
    model = PaymentMethod
    template_name = "paymentmethod_confirm_delete.html"
    success_url = reverse_lazy("payment_method_list")

    def dispatch(self, request, *args, **kwargs):
        method = self.get_object()
        if CashRegisterPayment.objects.filter(payment_method=method).exists():
            messages.error(request, "Este método de pagamento está em uso e não pode ser excluído.")
            return redirect("payment_method_list")
        return super().dispatch(request, *args, **kwargs)


# PDV

def pdv_payment_methods_sync(request):
    if request.headers.get("X-API-KEY") != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    methods = PaymentMethod.objects.filter(is_active=True, show_on_pdv=True).values(
        "id", "name", "is_cash", "is_credit", "is_machine_payment", "order"
    ).order_by("order")

    return JsonResponse({"payment_methods": list(methods)})
