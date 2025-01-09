from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView ,UpdateView
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class CustomerTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.CustomerType
    template_name = 'customer_type_list.html'
    context_object_name = 'customertypes'
    permission_required = 'customertypes.view_customertype'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class CustomerTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.CustomerType
    template_name = 'customer_type_form.html'
    form_class = forms.CustomerTypeForm
    success_url = reverse_lazy('customer_type_list')
    permission_required = 'customertypes.add_customertype'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class CustomerTypeDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.CustomerType
    template_name = 'customer_type_detail.html'
    permission_required = 'customertypes.view_customertype'

class CustomerTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.CustomerType
    template_name = 'customer_type_form.html'
    form_class = forms.CustomerTypeForm
    success_url = reverse_lazy('customer_type_list')
    permission_required = 'customertypes.change_customertype'


class CustomerStateListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.CustomerState
    template_name = 'customer_state_list.html'
    context_object_name = 'customerstates'
    permission_required = 'customerstates.view_customerstate'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class CustomerStateCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.CustomerState
    template_name = 'customer_state_form.html'
    form_class = forms.CustomerStateForm  # Certifique-se de ter um formulário correspondente
    success_url = reverse_lazy('customer_state_list')
    permission_required = 'customerstates.add_customerstate'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class CustomerStateDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.CustomerState
    template_name = 'customer_state_detail.html'
    permission_required = 'customerstates.view_customerstate'

class CustomerStateUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.CustomerState
    template_name = 'customer_state_form.html'
    form_class = forms.CustomerStateForm  # Certifique-se de ter um formulário correspondente
    success_url = reverse_lazy('customer_state_list')
    permission_required = 'customerstates.change_customerstate'


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'
    permission_required = 'customers.view_customers'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Customer
    template_name = 'customer_form.html'
    form_class = forms.CustomerForm
    success_url = reverse_lazy('customer_list')
    permission_required = 'customers.add_customers'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class CustomerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Customer
    template_name = 'customer_detail.html'
    permission_required = 'customers.view_customers'

class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Customer
    template_name = 'customer_form.html'
    form_class = forms.CustomerForm
    success_url = reverse_lazy('customer_list')
    permission_required = 'customers.change_customers'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
