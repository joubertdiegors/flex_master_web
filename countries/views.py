from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView ,UpdateView
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class CountryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Country
    template_name = 'country_list.html'
    context_object_name = 'countries'
    permission_required = 'countries.view_country'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class CountryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Country
    template_name = 'country_form.html'
    form_class = forms.CountryForm
    success_url = reverse_lazy('country_list')
    permission_required = 'countries.add_country'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class CountryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Country
    template_name = 'country_detail.html'
    permission_required = 'countries.view_country'

class CountryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Country
    template_name = 'country_form.html'
    form_class = forms.CountryForm
    success_url = reverse_lazy('country_list')
    permission_required = 'countries.change_country'