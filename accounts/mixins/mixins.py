from django.http import HttpResponseForbidden
from customers.models import Customer

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class CustomerAccessMixin:
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        customer_id = kwargs.get('customer_id')
        customer = Customer.objects.get(id=customer_id)

        if customer.user != request.user:
            return HttpResponseForbidden("Você não tem permissão para acessar esta página.")

        return super().dispatch(request, *args, **kwargs)
