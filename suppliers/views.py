from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView ,UpdateView
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class SupplierTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.SupplierType
    template_name = 'supplier_type_list.html'
    context_object_name = 'suppliertypes'
    permission_required = 'suppliertypes.view_suppliertype'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class SupplierTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.SupplierType
    template_name = 'supplier_type_form.html'
    form_class = forms.SupplierTypeForm
    success_url = reverse_lazy('supplier_type_list')
    permission_required = 'suppliertypes.add_suppliertype'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class SupplierTypeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.SupplierType
    template_name = 'supplier_type_detail.html'
    permission_required = 'suppliertypes.view_suppliertype'

class SupplierTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.SupplierType
    template_name = 'supplier_type_form.html'
    form_class = forms.SupplierTypeForm
    success_url = reverse_lazy('supplier_type_list')
    permission_required = 'suppliertypes.change_suppliertype'


class SupplierStateListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.SupplierState
    template_name = 'supplier_state_list.html'
    context_object_name = 'supplierstates'
    permission_required = 'supplierstates.view_supplierstate'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class SupplierStateCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.SupplierState
    template_name = 'supplier_state_form.html'
    form_class = forms.SupplierStateForm  # Certifique-se de ter um formulário correspondente
    success_url = reverse_lazy('supplier_state_list')
    permission_required = 'supplierstates.add_supplierstate'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class SupplierStateDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.SupplierState
    template_name = 'supplier_state_detail.html'
    permission_required = 'supplierstates.view_supplierstate'

class SupplierStateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.SupplierState
    template_name = 'supplier_state_form.html'
    form_class = forms.SupplierStateForm  # Certifique-se de ter um formulário correspondente
    success_url = reverse_lazy('supplier_state_list')
    permission_required = 'supplierstates.change_supplierstate'


class SupplierListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Supplier
    template_name = 'supplier_list.html'
    context_object_name = 'suppliers'
    permission_required = 'suppliers.view_supplier'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class SupplierCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Supplier
    template_name = 'supplier_form.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.add_supplier'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class SupplierDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Supplier
    template_name = 'supplier_detail.html'
    permission_required = 'suppliers.view_supplier'

class SupplierUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Supplier
    template_name = 'supplier_form.html'
    form_class = forms.SupplierForm
    success_url = reverse_lazy('supplier_list')
    permission_required = 'suppliers.change_supplier'
