from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse, HttpResponse
from . import models, forms


class SupplierProductPriceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.SupplierProductPrice
    template_name = 'supplier_product_price_list.html'
    context_object_name = 'supplier_product_prices'
    permission_required = 'suppliers.view_supplierproductprice'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add any filtering logic here
        return queryset
    
class SupplierProductPriceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.SupplierProductPrice
    template_name = 'supplier_product_price_form.html'
    form_class = forms.SupplierProductPriceForm
    success_url = reverse_lazy('supplier_product_price_list')
    permission_required = 'suppliers.add_supplierproductprice'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class SupplierProductPriceDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.SupplierProductPrice
    template_name = 'supplier_product_price_detail.html'
    context_object_name = 'supplier_product_price'
    permission_required = 'suppliers.view_supplierproductprice'

class SupplierProductPriceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.SupplierProductPrice
    template_name = 'supplier_product_price_form.html'
    form_class = forms.SupplierProductPriceForm
    success_url = reverse_lazy('supplier_product_price_list')
    permission_required = 'suppliers.change_supplierproductprice'


class PurchaseOrderListView(ListView):
    model = models.PurchaseOrder
    template_name = 'purchase_order_list.html'
    context_object_name = 'purchase_orders'

class PurchaseOrderCreateView(CreateView):
    model = models.PurchaseOrder
    form_class = forms.PurchaseOrderForm
    template_name = 'purchase_order_form.html'
    success_url = reverse_lazy('purchase_order_list')

    def get_initial(self):
        initial = super().get_initial()
        initial['order_number'] = models.PurchaseOrder().generate_order_number()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = forms.PurchaseOrderItemFormSet(self.request.POST)
        else:
            context['items'] = forms.PurchaseOrderItemFormSet()
        context['products'] = models.Product.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        form.instance.created_by = self.request.user
        self.object = form.save()

        # Log the POST data to see what is being submitted
        print("POST data:", self.request.POST)

        if items.is_valid():
            items.instance = self.object
            items.save()
            return super().form_valid(form)
        else:
            # Print the errors to the console for debugging
            print("Formset is not valid:")
            print(items.errors)
            # Re-render the page with formset errors
            return self.render_to_response(self.get_context_data(form=form))
        
    def form_invalid(self, form):
        # Se o formulário principal for inválido, re-renderize a página com os erros
        print("Form is not valid:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class PurchaseOrderUpdateView(UpdateView):
    model = models.PurchaseOrder
    form_class = forms.PurchaseOrderForm
    template_name = 'purchase_order_form.html'
    success_url = reverse_lazy('purchase_order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items'] = forms.PurchaseOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items'] = forms.PurchaseOrderItemFormSet(instance=self.object)
        context['products'] = models.Product.objects.all()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        form.instance.updated_by = self.request.user
        self.object = form.save()

        if items.is_valid():
            items.instance = self.object
            items.save()
            return super().form_valid(form)
        else:
            # Debugging: Print the errors to see what's going wrong
            for formset_error in items.errors:
                print(formset_error)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print("Form is not valid:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class PurchaseOrderDeleteView(DeleteView):
    model = models.PurchaseOrder
    template_name = 'purchase_order_confirm_delete.html'
    success_url = reverse_lazy('purchase_order_list')

def get_product_price(request):
    supplier_id = request.GET.get('supplier_id')
    product_id = request.GET.get('product_id')
    
    try:
        # Busca o preço do produto para o fornecedor específico
        price = models.SupplierProductPrice.objects.get(supplier_id=supplier_id, product_id=product_id).purchase_price
        return JsonResponse({'price': price}, status=200)
    except models.SupplierProductPrice.DoesNotExist:
        return JsonResponse({'error': 'Preço não encontrado para o fornecedor e produto selecionados'}, status=404)
