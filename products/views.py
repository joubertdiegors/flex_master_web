from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Func, F
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from dal import autocomplete
from django.db import connection
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class BrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Brand
    template_name = 'brand_list.html'
    context_object_name = 'brands'
    permission_required = 'brands.view_brand'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset

class BrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Brand
    template_name = 'brand_form.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.add_brand'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class BrandDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Brand
    template_name = 'brand_detail.html'
    context_object_name = 'brand'
    permission_required = 'brands.view_brand'

class BrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Brand
    template_name = 'brand_form.html'
    form_class = forms.BrandForm
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.update_brand'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class BrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Brand
    template_name = 'brand_delete.html'
    success_url = reverse_lazy('brand_list')
    permission_required = 'brands.delete_brand'


class SalesUnitListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.SalesUnit
    template_name = 'sales_unit_list.html'
    context_object_name = 'sales_units'
    permission_required = 'salesunits.view_salesunit'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset

class SalesUnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.SalesUnit
    template_name = 'sales_unit_form.html'
    form_class = forms.SalesUnitForm
    success_url = reverse_lazy('sales_unit_list')
    permission_required = 'salesunits.add_salesunit'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class SalesUnitDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.SalesUnit
    template_name = 'sales_unit_detail.html'
    context_object_name = 'sales_unit'
    permission_required = 'salesunits.view_salesunit'

class SalesUnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.SalesUnit
    template_name = 'sales_unit_form.html'
    form_class = forms.SalesUnitForm
    success_url = reverse_lazy('sales_unit_list')
    permission_required = 'salesunits.change_salesunit'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class SalesUnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.SalesUnit
    template_name = 'sales_unit_delete.html'
    success_url = reverse_lazy('sales_unit_list')
    permission_required = 'salesunits.delete_salesunit'


class PackageUnitListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.PackageUnit
    template_name = 'package_unit_list.html'
    context_object_name = 'package_units'
    permission_required = 'packageunits.view_packageunit'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name__icontains=name)
        
        return queryset

class PackageUnitCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.PackageUnit
    template_name = 'package_unit_form.html'
    form_class = forms.PackageUnitForm
    success_url = reverse_lazy('package_unit_list')
    permission_required = 'packageunits.add_packageunit'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class PackageUnitDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.PackageUnit
    template_name = 'package_unit_detail.html'
    context_object_name = 'package_unit'
    permission_required = 'packageunits.view_packageunit'

class PackageUnitUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.PackageUnit
    template_name = 'package_unit_form.html'
    form_class = forms.PackageUnitForm
    success_url = reverse_lazy('package_unit_list')
    permission_required = 'packageunits.change_packageunit'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class PackageUnitDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.PackageUnit
    template_name = 'package_unit_delete.html'
    success_url = reverse_lazy('package_unit_list')
    permission_required = 'packageunits.delete_packageunit'


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    permission_required = 'products.view_product'

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Product
    template_name = 'product_form.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.add_product'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    permission_required = 'products.view_product'

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Product
    template_name = 'product_form.html'
    form_class = forms.ProductForm
    success_url = reverse_lazy('product_list')
    permission_required = 'products.change_product'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'products.delete_product'
    
def product_search(request):
    query = request.GET.get('q', '')
    print(f"Search query: {query}")

    if query:
        products = models.Product.objects.filter(name__icontains=query)[:10]
        
        if not products.exists():
            print(f"No products found for query: {query}")

        results = [{'id': product.id, 'name': product.name} for product in products]
        print(f"Products found: {results}")
    else:
        results = []
        print("No query provided, returning empty list.")
    
    return JsonResponse({'products': results})


class IngredientsCreateView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'ingredients_form.html'
    permission_required = 'ingredients.view_ingredient'
    
    def get(self, request, pk=None):
        product = get_object_or_404(models.Product, pk=pk)
        ingredients = models.Ingredients.objects.filter(product=product)
        if ingredients.exists():
            form = forms.IngredientsForm(instance=ingredients.first())
        else:
            form = forms.IngredientsForm(initial={'product': product})
        return render(request, self.template_name, {'form': form, 'product': product})

    def post(self, request, pk=None):
        product = get_object_or_404(models.Product, pk=pk)
        ingredients = models.Ingredients.objects.filter(product=product)
        if ingredients.exists():
            form = forms.IngredientsForm(request.POST, instance=ingredients.first())
        else:
            form = forms.IngredientsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, self.template_name, {'form': form, 'product': product})


class NutritionalItemListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.NutritionalItem
    template_name = 'nutritional_item_list.html'
    context_object_name = 'nutritional_items'
    permission_required = 'nutritionalitems.view_nutritionalitem'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        return queryset

class NutritionalItemCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.NutritionalItem
    template_name = 'nutritional_item_form.html'
    form_class = forms.NutritionalItemForm
    success_url = reverse_lazy('nutritional_item_list')
    permission_required = 'nutritionalitems.add_nutritionalitem'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class NutritionalItemUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.NutritionalItem
    template_name = 'nutritional_item_form.html'
    form_class = forms.NutritionalItemForm
    success_url = reverse_lazy('nutritional_item_list')
    permission_required = 'nutritionalitems.change_nutritionalitem'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class NutritionalItemDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.NutritionalItem
    template_name = 'nutritional_item_delete.html'
    success_url = reverse_lazy('nutritional_item_list')
    permission_required = 'nutritionalitems.delete_nutritionalitem'


class NutritionalInfoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'nutritional_info_form.html'
    permission_required = 'nutritionalinfos.view_nutritionalinfo'
    
    def get(self, request, pk=None):
        product = get_object_or_404(models.Product, pk=pk)
        formset = forms.NutritionalInfoFormSet(instance=product)
        return render(request, self.template_name, {'formset': formset, 'product': product})

    def post(self, request, pk=None):
        product = get_object_or_404(models.Product, pk=pk)
        formset = forms.NutritionalInfoFormSet(request.POST, instance=product)

        if formset.is_valid():
            formset.save()
            return redirect(reverse('nutritional_info_create', kwargs={'pk': product.pk}))
        else:
            print("Formset is not valid:", formset.errors)
        
        return render(request, self.template_name, {'formset': formset, 'product': product})

class NutritionalInfoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.NutritionalInfo
    permission_required = 'nutritionalinfos.delete_nutritionalinfo'

    def get_success_url(self):
        product_id = self.object.product.id
        return reverse('nutritional_info_create', kwargs={'pk': product_id})


#### PDV Local ###

def pdv_products_sync(request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")
    
    data = []
    for p in models.Product.objects.filter(is_active=True).prefetch_related("category"):
        data.append({
            "id": p.id,
            "name": p.name,
            "barcode": p.barcode,
            "selling_price": float(p.selling_price),
            "stock_quantity": float(p.stock_quantity),
            "brand_id": p.brand_id,
            "sales_unit": p.sales_unit_id,
            "categories": list(p.category.values_list("id", flat=True)),
        })

    return JsonResponse({"products": data})

def pdv_brands_sync(request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")
    
    brands = models.Brand.objects.all().values("id", "name")
    return JsonResponse({"brands": list(brands)})

def pdv_units_sync(request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")
    
    units = models.SalesUnit.objects.all().values("id", "name", "symbol", "is_fractional")
    return JsonResponse({"units": list(units)})

def pdv_product_category_relations(request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != settings.PDV_API_KEY:
        return HttpResponseForbidden("Unauthorized")

    # Acessa a tabela ManyToMany diretamente
    relations = models.Product.category.through.objects.all().values("product_id", "category_id")
    return JsonResponse({"relations": list(relations)})
