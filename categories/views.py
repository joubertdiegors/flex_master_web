from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from . import models
from . import forms

class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Category
    template_name = 'category_list.html'
    context_object_name = 'categories'
    permission_required = 'categories.view_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_form'] = forms.CategoryForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
def category_list_json(request):
    categories = models.Category.objects.all().values('id', 'name', 'parent')
    data = list(categories)
    return JsonResponse(data, safe=False)

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'category_list.html'
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.add_category'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Categoria criada com sucesso!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao criar a categoria. Por favor, verifique e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))

class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Category
    template_name = 'category_list.html'
    form_class = forms.CategoryForm
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.change_category'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Falha ao atualizar a categoria. Por favor, verifique e tente novamente.')
        return self.render_to_response(self.get_context_data(form=form))

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Category
    success_url = reverse_lazy('category_list')
    permission_required = 'categories.delete_category'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, 'Categoria excluída com sucesso!')
            return JsonResponse({'success': True})
        except ProtectedError as e:
            messages.error(request, 'Erro ao excluir a categoria! Verifique se a categoria não tem uma subcategoria vinculada')
            return JsonResponse({'error': str(e)}, status=400)

