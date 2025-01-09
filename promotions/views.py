from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Promotion
from .forms import PromotionForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PromotionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Promotion
    template_name = 'promotion_list.html'
    context_object_name = 'promotions'
    permission_required = 'promotions.view_promotion'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class PromotionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Promotion
    template_name = 'promotion_form.html'
    form_class = PromotionForm
    success_url = reverse_lazy('promotion_list')
    permission_required = 'promotions.add_promotion'

    def form_valid(self, form):
        # Lógica adicional ao salvar o formulário, se necessário
        return super().form_valid(form)

class PromotionDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Promotion
    template_name = 'promotion_detail.html'
    permission_required = 'promotions.view_promotion'

class PromotionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Promotion
    template_name = 'promotion_form.html'
    form_class = PromotionForm
    success_url = reverse_lazy('promotion_list')
    permission_required = 'promotions.change_promotion'

class PromotionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Promotion
    success_url = reverse_lazy('promotion_list')
    permission_required = 'promotions.delete_promotion'
