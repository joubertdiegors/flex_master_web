import os
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from unidecode import unidecode
from django.views.generic import View, DetailView
from products.models import Product, Brand, Ingredients, NutritionalInfo
from promotions.models import Promotion
from categories.models import Category
from countries.models import Country
from customization_store.models import Banner, HighlightedBrand, BestSellerProduct, FreshProducts

class StoreHomeView(View):
    template_name = 'store_home.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        highlighted_brands = HighlightedBrand.objects.filter(is_active=True)
        countries = Country.objects.all()
        banners = Banner.objects.all()
        best_seller_products = list(BestSellerProduct.objects.all())
        fresh_products = list(FreshProducts.objects.all())
        promotions = list(Promotion.objects.all())
        
        context = {
            'products': products,
            'categories': categories,
            'highlighted_brands': highlighted_brands,
            'countries': countries,
            'banners': banners,
            'best_seller_products': best_seller_products,
            'fresh_products': fresh_products,
            'promotions': promotions,
            'is_not_list_page': True,
            'breadcrumb_off': True,
            'custom_content': load_custom_content(),
        }
        return render(request, self.template_name, context)
    
class StoreProductListView(View):
    template_name = 'store_product_list.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()

        # Pegando o valor de produtos por página do request, ou definindo o padrão como 16
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)

        paginator = Paginator(products, products_per_page)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'categories': categories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,
        }
        return render(request, self.template_name, context)

class ProductsByCategoryView(View):
    template_name = 'store_product_list.html'

    def get(self, request, category_path, *args, **kwargs):
        # Divide o caminho da categoria em uma lista
        category_names = category_path.strip('/').split('/')
        
        # Inicializa a categoria atual como None
        current_category = None
        ancestors = []  # Lista para armazenar categorias ancestrais

        # Itera sobre os nomes das categorias para encontrar a categoria correta
        for category_name in category_names:
            if current_category:
                current_category = get_object_or_404(Category, name=category_name, parent=current_category)
            else:
                current_category = get_object_or_404(Category, name=category_name, parent__isnull=True)
            ancestors.append(current_category)  # Adiciona a categoria à lista de ancestrais
        
        # Obtenha os produtos da categoria atual
        products = Product.objects.filter(category=current_category)
        
        # Obtenha todas as categorias de nível superior para o menu de navegação
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        
        # Obtenha todas as marcas e países
        brands = Brand.objects.all()
        countries = Country.objects.all()
        
        # Pegue o valor de produtos por página do request, ou defina o padrão como 16
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)
        
        paginator = Paginator(products, products_per_page)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Obtenha as subcategorias da categoria atual
        subcategories = current_category.subcategories.all()
        
        context = {
            'selected_category': current_category,
            'selected_categories': ancestors,  # Passa a lista de categorias ancestrais para o template
            'products': page_obj,
            'categories': categories,
            'subcategories': subcategories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,
        }
        return render(request, self.template_name, context)

class ProductsByBrandView(View):
    template_name = 'store_product_list.html'

    def get(self, request, brand_name, *args, **kwargs):
        brand = get_object_or_404(Brand, name=brand_name)
        products = Product.objects.filter(brand=brand)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()

        # Pegando o valor de produtos por página do request, ou definindo o padrão como 16
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)

        paginator = Paginator(products, products_per_page)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'selected_brand': brand,
            'categories': categories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,
        }
        return render(request, self.template_name, context)

class ProductsByCountryView(View):
    template_name = 'store_product_list.html'

    def get(self, request, country_name, *args, **kwargs):
        country = get_object_or_404(Country, name=country_name)
        products = Product.objects.filter(country=country)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()

        # Pegando o valor de produtos por página do request, ou definindo o padrão como 16
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)

        paginator = Paginator(products, products_per_page)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'selected_country': country,
            'categories': categories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,
        }
        return render(request, self.template_name, context)

class SearchProductView(View):
    template_name = 'store_product_list.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('q')
        products = Product.objects.all()
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()

        # Pegando o valor de produtos por página do request, ou definindo o padrão como 16
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)

        paginator = Paginator(products, products_per_page)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        if search_query:
            print(f"Search query received: {search_query}")

            # Aplica unidecode na consulta
            normalized_query = unidecode(search_query)

            # Filtra produtos onde o nome contém o termo de pesquisa (com ou sem acentos) e também por marca
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(name__icontains=normalized_query) |
                Q(brand__name__icontains=search_query) |
                Q(brand__name__icontains=normalized_query)
            )

            context = {
                'products': products,
                'categories': categories,
                'brands': brands,
                'countries': countries,
                'search_query': search_query,
                'page_obj': page_obj,
                'products_per_page': products_per_page,
            }
        else:
            context = {
                'products': page_obj,
                'categories': categories,
                'brands': brands,
                'countries': countries,
                'page_obj': page_obj,
                'products_per_page': products_per_page,
            }

        return render(request, self.template_name, context)

class StoreProductBestSellerView(View):
    template_name = 'store_product_best_seller.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()
        best_seller_products = BestSellerProduct.objects.all()

        # Obtendo os produtos correspondentes aos produtos mais vendidos
        products = [best_seller.product for best_seller in best_seller_products]

        # Paginação dos produtos
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)
        paginator = Paginator(products, products_per_page)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'categories': categories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,  # Supondo que esta função retorna URLs de logos
            'is_best_seller_page': True,
        }
        return render(request, self.template_name, context)

class StoreProductFreshListView(View):
    template_name = 'store_product_fresh_list.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()

        # Obtendo os produtos novos
        fresh_products = FreshProducts.objects.all()

        # Obtendo os produtos correspondentes aos produtos novos
        products = [fresh_product.product for fresh_product in fresh_products]

        # Paginação dos produtos
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)
        paginator = Paginator(products, products_per_page)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'categories': categories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,  # Supondo que esta função retorna URLs de logos
            'is_fresh_list_page': True,
            
        }
        return render(request, self.template_name, context)

class StoreProductPromotionsView(View):
    template_name = 'store_product_promotions.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        brands = Brand.objects.all()
        countries = Country.objects.all()
        promotions = Promotion.objects.all()

        products = [promotion.product for promotion in promotions]

        # Paginação dos produtos
        products_per_page = request.GET.get('products_per_page', 16)
        products_per_page = int(products_per_page)
        paginator = Paginator(products, products_per_page)
        
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'categories': categories,
            'brands': brands,
            'countries': countries,
            'page_obj': page_obj,
            'products_per_page': products_per_page,
            'is_promotions_list_page': True,
        }
        return render(request, self.template_name, context)

class StoreProductDetailView(View):
    template_name = 'store_product_detail.html'

    def get(self, request, pk, product_name, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        nutritional_info = NutritionalInfo.objects.filter(product=product)

        # Recupera os ingredientes associados ao produto, se existirem
        try:
            ingredients = Ingredients.objects.get(product=product)
        except Ingredients.DoesNotExist:
            ingredients = None

        # Adiciona informações de categoria e subcategoria
        selected_categories = product.category.all()

        context = {
            'product': product,
            'categories': categories,
            'selected_categories': selected_categories,
            'ingredients': ingredients,
            'nutritional_infos': nutritional_info,
            'is_not_list_page': True,
            'is_detail_page': True,
        }
        return render(request, self.template_name, context)

class AboutUsView(View):
    template_name = 'store_about_us.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

class DeliveryInfoView(View):
    template_name = 'store_delivery_info.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

class PrivacyPolicyView(View):
    template_name = 'store_privacy_policy.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)
    
def load_custom_content():
    with open(os.path.join(settings.BASE_DIR, 'customization_store/templates/content.json'), 'r', encoding='utf-8') as f:
        return json.load(f)
