from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView ,UpdateView
from . import models, forms


class BranchListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Branch
    template_name = 'branch_list.html'
    context_object_name = 'branches'
    permission_required = 'branches.view_branch'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset
    
class BranchCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Branch
    template_name = 'branch_form.html'
    form_class = forms.BranchForm
    success_url = reverse_lazy('branch_list')
    permission_required = 'branches.add_branch'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class BranchDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Branch
    template_name = 'branch_detail.html'
    permission_required = 'branches.view_branch'

class BranchUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Branch
    template_name = 'branch_form.html'
    form_class = forms.BranchForm
    success_url = reverse_lazy('branch_list')
    permission_required = 'branches.change_branch'