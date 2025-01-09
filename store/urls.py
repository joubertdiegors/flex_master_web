from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreHomeView.as_view(), name='store_home'),
    
    path('loja/promocoes/', views.StoreProductPromotionsView.as_view(), name='store_product_promotions_list'),
    path('loja/mais_vendidos/', views.StoreProductBestSellerView.as_view(), name='store_product_best_seller_list'),
    path('loja/novidades/', views.StoreProductFreshListView.as_view(), name='store_product_fresh_list'),

    path('loja/', views.StoreProductListView.as_view(), name='store_product_list'),
    path('loja/<path:category_path>/', views.ProductsByCategoryView.as_view(), name='store_products_by_category'),

    path('marcas/<str:brand_name>/', views.ProductsByBrandView.as_view(), name='store_products_by_brand'),
    path('paises/<str:country_name>/', views.ProductsByCountryView.as_view(), name='store_products_by_country'),
    path('busca/', views.SearchProductView.as_view(), name='search_product'),
    path('produto/<int:pk>/<str:product_name>/', views.StoreProductDetailView.as_view(), name='store_product_detail'),

    path('sobre-nos/', views.AboutUsView.as_view(), name='about_us'),
    path('informacoes-de-entrega/', views.DeliveryInfoView.as_view(), name='delivery_info'),
    path('politica-de-privacidade/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
]