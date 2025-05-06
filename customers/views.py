from django.conf import settings
from datetime import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView ,UpdateView, View, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, HttpResponseForbidden
from . import models, forms
from products.models import Category

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

class CustomerProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_profile.html'

    def get(self, request, *args, **kwargs):
        customer = self.request.user.customer_profile
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'customer': customer,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)    

class CustomerProfileUpdateView(LoginRequiredMixin, View):
    template_name = 'customer_profile_update.html'
    form_class = forms.CustomerProfileUpdateForm
    success_url = reverse_lazy('customer_profile')

    def get(self, request, *args, **kwargs):
        customer = request.user.customer_profile
        form = self.form_class(instance=customer)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        
        # Adiciona as informações ao contexto
        categories = Category.objects.all()
        context = {
            'form': form,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        customer = request.user.customer_profile
        form = self.form_class(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            birth_date_str = form.cleaned_data.get('birth_date')
            if birth_date_str:
                try:
                    birth_date_str = birth_date_str.strftime('%Y-%m-%d')
                    customer.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            form.save()
            return redirect('customer_profile')  # Redireciona para a página de conta do cliente

        return render(request, self.template_name, {'form': form})


# PDV

def pdv_customers_sync(request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    customers = models.Customer.objects.all().values(
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "birth_date",
        "company_name",
        "tva_number",
        "contact_person_name",
        "contact_person_phone",
        "contact_person_email",
        "other_email",
        "country_id",
        "postal_code",
        "city",
        "address",
        "status_id",
        "customer_type_id",
    )

    return JsonResponse({"customers": list(customers)})
