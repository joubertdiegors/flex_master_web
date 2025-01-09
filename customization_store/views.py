import os
import json
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from PIL import Image as PILImage
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .forms import HeaderLogoForm, NavbarLogoForm, FaviconForm, ProductImageForm, CustomerImageForm, SupplierImageForm, BannerForm
from . import models, forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import GlobalSettings

def maintenance_view(request):
    settings = GlobalSettings.objects.first()
    message = settings.maintenance_message if settings else "Manutenção em andamento."
    return render(request, 'maintenance.html', {'message': message})

class CustomizationHomeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = 'customization_home.html'
    permission_required = 'customizationshome.view_customizationhome'

    def get(self, request, *args, **kwargs):
        header_logo_url = None
        navbar_logo_url = None
        favicon_url = None
        product_default_url = None
        customer_default_url = None
        supplier_default_url = None
        timestamp = datetime.now().timestamp()

        logo_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        header_logo_path = os.path.join(logo_dir, 'header_logo.png')
        navbar_logo_path = os.path.join(logo_dir, 'navbar_logo.png')
        product_default_path = os.path.join(logo_dir, 'product_default.png')
        customer_default_path = os.path.join(logo_dir, 'customer_default.png')
        supplier_default_path = os.path.join(logo_dir, 'supplier_default.png')
        favicon_path = os.path.join(logo_dir, 'favicon.ico')

        if os.path.exists(header_logo_path):
            header_logo_url = settings.MEDIA_URL + 'store/logo/header_logo.png'

        if os.path.exists(navbar_logo_path):
            navbar_logo_url = settings.MEDIA_URL + 'store/logo/navbar_logo.png'

        if os.path.exists(product_default_path):
            product_default_url = settings.MEDIA_URL + 'store/logo/product_default.png'

        if os.path.exists(customer_default_path):
            customer_default_url = settings.MEDIA_URL + 'store/logo/customer_default.png'

        if os.path.exists(supplier_default_path):
            supplier_default_url = settings.MEDIA_URL + 'store/logo/supplier_default.png'

        if os.path.exists(favicon_path):
            favicon_url = settings.MEDIA_URL + 'store/logo/favicon.ico'

        context = {
            'header_form': HeaderLogoForm(),
            'header_logo_url': header_logo_url,
            'navbar_form': NavbarLogoForm(),
            'navbar_logo_url': navbar_logo_url,
            'favicon_form': FaviconForm(),
            'favicon_url': favicon_url,
            'product_form': ProductImageForm(),
            'product_default_url': product_default_url,
            'customer_form': CustomerImageForm(),
            'customer_default_url': customer_default_url,
            'supplier_form': SupplierImageForm(),
            'supplier_default_url': supplier_default_url,
            'timestamp': timestamp,
        }
        return render(request, self.template_name, context)


class UploadHeaderLogoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'uploadheaderlogo.view_uploadheaderlogo'

    def post(self, request, *args, **kwargs):
        logo_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        header_logo_path = os.path.join(logo_dir, 'header_logo.png')

        header_form = HeaderLogoForm(request.POST, request.FILES)
        if header_form.is_valid():
            header_logo = request.FILES['header_logo']

            if not os.path.exists(logo_dir):
                os.makedirs(logo_dir)

            # Remover o logo antigo, se existir
            if os.path.exists(header_logo_path):
                os.remove(header_logo_path)

            # Salvar o novo logo
            with open(header_logo_path, 'wb+') as destination:
                for chunk in header_logo.chunks():
                    destination.write(chunk)

            # Redimensionar a imagem se necessário
            img = PILImage.open(header_logo_path)
            img.thumbnail((img.width, 200))
            img.save(header_logo_path)

        return redirect('customization_home')

class UploadNavbarLogoView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'uploadnavbarlogo.view_uploadnavbarlogo'

    def post(self, request, *args, **kwargs):
        logo_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        navbar_logo_path = os.path.join(logo_dir, 'navbar_logo.png')
        print("Teste")

        navbar_form = NavbarLogoForm(request.POST, request.FILES)
        if navbar_form.is_valid():
            navbar_logo = request.FILES['navbar_logo']

            if not os.path.exists(logo_dir):
                os.makedirs(logo_dir)

            # Remover o logo antigo, se existir
            if os.path.exists(navbar_logo_path):
                os.remove(navbar_logo_path)

            # Salvar o novo logo
            with open(navbar_logo_path, 'wb+') as destination:
                for chunk in navbar_logo.chunks():
                    destination.write(chunk)

            # Redimensionar a imagem se necessário
            img = PILImage.open(navbar_logo_path)
            img.thumbnail((img.width, 70))
            img.save(navbar_logo_path)

        return redirect('customization_home')

class UploadFaviconView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'uploadfavicon.view_uploadfavicon'

    def post(self, request, *args, **kwargs):
        logo_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        favicon_path = os.path.join(logo_dir, 'favicon.ico')

        favicon_form = FaviconForm(request.POST, request.FILES)
        if favicon_form.is_valid():
            favicon = request.FILES['favicon']

            if not os.path.exists(logo_dir):
                os.makedirs(logo_dir)

            # Remover o favicon antigo, se existir
            if os.path.exists(favicon_path):
                os.remove(favicon_path)

            # Salvar o novo favicon
            temp_path = os.path.join(logo_dir, 'temp_favicon')
            with open(temp_path, 'wb+') as destination:
                for chunk in favicon.chunks():
                    destination.write(chunk)

            # Redimensionar a imagem para 16x16 pixels
            img = PILImage.open(temp_path)
            img = img.resize((16, 16), PILImage.LANCZOS)
            img.save(favicon_path, format='ICO')

            # Remover o arquivo temporário
            os.remove(temp_path)

        return redirect('customization_home')

class UploadProductImageDefaultView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'uploadproductimagedefaultlogo.view_uploadproductimagedefaultlogo'

    def post(self, request, *args, **kwargs):
        image_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        product_image_path = os.path.join(image_dir, 'product_default.png')

        product_form = ProductImageForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_image = request.FILES['product_default']

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Remover a imagem antiga, se existir
            if os.path.exists(product_image_path):
                os.remove(product_image_path)

            # Salvar a nova imagem
            with open(product_image_path, 'wb+') as destination:
                for chunk in product_image.chunks():
                    destination.write(chunk)

            # Redimensionar a imagem se necessário
            img = PILImage.open(product_image_path)
            img.thumbnail((img.width, 200))
            img.save(product_image_path)

        return redirect('customization_home')

class UploadCustomerImageDefaultView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'uploadcustomerimagedefaultlogo.view_uploadcustomerimagedefaultlogo'

    def post(self, request, *args, **kwargs):
        image_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        customer_image_path = os.path.join(image_dir, 'customer_default.png')

        customer_form = CustomerImageForm(request.POST, request.FILES)
        if customer_form.is_valid():
            product_image = request.FILES['customer_default']

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Remover a imagem antiga, se existir
            if os.path.exists(customer_image_path):
                os.remove(customer_image_path)

            # Salvar a nova imagem
            with open(customer_image_path, 'wb+') as destination:
                for chunk in product_image.chunks():
                    destination.write(chunk)

            # Redimensionar a imagem se necessário
            img = PILImage.open(customer_image_path)
            img.thumbnail((img.width, 200))
            img.save(customer_image_path)

        return redirect('customization_home')

class UploadSupplierImageDefaultView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'uploadsupplierimagedefaultlogo.view_uploadsupplierimagedefaultlogo'

    def post(self, request, *args, **kwargs):
        image_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
        supplier_image_path = os.path.join(image_dir, 'supplier_default.png')

        supplier_form = SupplierImageForm(request.POST, request.FILES)
        if supplier_form.is_valid():
            product_image = request.FILES['supplier_default']

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            # Remover a imagem antiga, se existir
            if os.path.exists(supplier_image_path):
                os.remove(supplier_image_path)

            # Salvar a nova imagem
            with open(supplier_image_path, 'wb+') as destination:
                for chunk in product_image.chunks():
                    destination.write(chunk)

            # Redimensionar a imagem se necessário
            img = PILImage.open(supplier_image_path)
            img.thumbnail((img.width, 200))
            img.save(supplier_image_path)

        return redirect('customization_home')


class BannerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Banner
    template_name = 'banner_list.html'
    context_object_name = 'banners'
    permission_required = 'banners.view_banner'

    def get_queryset(self):
        queryset = super().get_queryset()
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

class BannerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Banner
    template_name = 'banner_create.html'
    form_class = BannerForm
    success_url = reverse_lazy('banner_list')
    permission_required = 'banners.add_banner'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class BannerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Banner
    template_name = 'banner_create.html'
    form_class = BannerForm
    success_url = reverse_lazy('banner_list')
    permission_required = 'banners.change_banner'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class BannerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Banner
    success_url = reverse_lazy('banner_list')
    permission_required = 'banners.delete_banner'


class BestSellerProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.BestSellerProduct
    template_name = 'best_seller_list.html'
    context_object_name = 'best_sellers'
    permission_required = 'bestsellersproduct.view_bestsellerproduct'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(product__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

class BestSellerProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.BestSellerProduct
    template_name = 'best_seller_form.html'
    form_class = forms.BestSellerProductForm
    success_url = reverse_lazy('best_seller_list')
    permission_required = 'bestsellersproduct.add_bestsellerproduct'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class BestSellerProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.BestSellerProduct
    template_name = 'best_seller_form.html'
    form_class = forms.BestSellerProductForm
    success_url = reverse_lazy('best_seller_list')
    permission_required = 'bestsellersproduct.change_bestsellerproduct'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class BestSellerProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.BestSellerProduct
    success_url = reverse_lazy('best_seller_list')
    permission_required = 'bestsellersproduct.delete_bestsellerproduct'


class FreshProductsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.FreshProducts
    template_name = 'fresh_product_list.html'
    context_object_name = 'fresh_products'
    permission_required = 'freshproducts.view_freshproduct'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(product__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

class FreshProductsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.FreshProducts
    template_name = 'fresh_product_form.html'
    form_class = forms.FreshProductsForm
    success_url = reverse_lazy('fresh_product_list')
    permission_required = 'freshproducts.add_freshproduct'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class FreshProductsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.FreshProducts
    template_name = 'fresh_product_form.html'
    form_class = forms.FreshProductsForm
    success_url = reverse_lazy('fresh_product_list')
    permission_required = 'freshproducts.change_freshproduct'

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class FreshProductsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.FreshProducts
    success_url = reverse_lazy('fresh_product_list')
    permission_required = 'freshproducts.delete_freshproduct'


class HighlightedBrandListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.HighlightedBrand
    template_name = 'highlighted_brand_list.html'
    context_object_name = 'highlighted_brands'
    permission_required = 'highlightedbrands.view_highlightedbrand'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(brand__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset

class HighlightedBrandCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.HighlightedBrand
    template_name = 'highlighted_brand_form.html'
    form_class = forms.HighlightedBrandForm
    success_url = reverse_lazy('highlighted_brand_list')
    permission_required = 'highlightedbrands.add_highlightedbrand'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class HighlightedBrandUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.HighlightedBrand
    template_name = 'highlighted_brand_form.html'
    form_class = forms.HighlightedBrandForm
    success_url = reverse_lazy('highlighted_brand_list')
    permission_required = 'highlightedbrands.change_highlightedbrand'

    def form_valid(self, form):
        return super().form_valid(form)

class HighlightedBrandDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.HighlightedBrand
    success_url = reverse_lazy('highlighted_brand_list')
    permission_required = 'highlightedbrands.delete_highlightedbrand'


# Conteúdo das informações de envio da home
def load_content():
    try:
        with open(os.path.join(settings.BASE_DIR, 'customization_store/templates/content.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except UnicodeDecodeError:
        with open(os.path.join(settings.BASE_DIR, 'customization_store/templates/content.json'), 'r', encoding='latin-1') as f:
            return json.load(f)

def save_content(content):
    with open(os.path.join(settings.BASE_DIR, 'customization_store/templates/content.json'), 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

def edit_content(request):
    if request.method == 'POST':
        content = load_content()
        for section in content.keys():
            content[section]['title'] = request.POST.get(f'{section}_title', content[section]['title'])
            content[section]['content'] = request.POST.get(f'{section}_content', content[section]['content'])
        save_content(content)
        messages.success(request, 'Conteúdo atualizado com sucesso!')
        return redirect('edit_content')
    
    content = load_content()
    return render(request, 'edit_content.html', {'content': content})