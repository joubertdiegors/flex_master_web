from django.urls import path
from . import views
from .views import maintenance_view

urlpatterns = [
    path('maintenance/', maintenance_view, name='maintenance'),

    path('administration/customization/', views.CustomizationHomeView.as_view(), name='customization_home'),

    path('administration/customization/header/', views.UploadHeaderLogoView.as_view(), name='upload_header_logo'),
    path('administration/customization/navbar/', views.UploadNavbarLogoView.as_view(), name='upload_navbar_logo'),
    path('administration/customization/favicon/', views.UploadFaviconView.as_view(), name='upload_favicon'),
    path('administration/customization/product_default/', views.UploadProductImageDefaultView.as_view(), name='upload_product_image_default'),
    path('administration/customization/customer_default/', views.UploadCustomerImageDefaultView.as_view(), name='upload_customer_image_default'),
    path('administration/customization/supplier_default/', views.UploadSupplierImageDefaultView.as_view(), name='upload_supplier_image_default'),
    path('administration/shipping_information/home/edit/', views.edit_content, name='edit_content'),

    path('administration/customization/banner/list/', views.BannerListView.as_view(), name='banner_list'),
    path('administration/customization/banner/create/', views.BannerCreateView.as_view(), name='banner_create'),
    path('administration/customization/banner/<int:pk>/edit/', views.BannerUpdateView.as_view(), name='banner_update'),
    path('administration/customization/banner/delete/<int:pk>/', views.BannerDeleteView.as_view(), name='banner_delete'),

    path('administration/customization/best_sellers/', views.BestSellerProductListView.as_view(), name='best_seller_list'),
    path('administration/customization/best_sellers/new/', views.BestSellerProductCreateView.as_view(), name='best_seller_create'),
    path('administration/customization/best_sellers/<int:pk>/edit/', views.BestSellerProductUpdateView.as_view(), name='best_seller_update'),
    path('administration/customization/best_sellers/<int:pk>/delete/', views.BestSellerProductDeleteView.as_view(), name='best_seller_delete'),

    path('administration/customization/fresh_products/', views.FreshProductsListView.as_view(), name='fresh_product_list'),
    path('administration/customization/fresh_products/new/', views.FreshProductsCreateView.as_view(), name='fresh_product_create'),
    path('administration/customization/fresh_products/<int:pk>/edit/', views.FreshProductsUpdateView.as_view(), name='fresh_product_update'),
    path('administration/customization/fresh_products/<int:pk>/delete/', views.FreshProductsDeleteView.as_view(), name='fresh_product_delete'),

    path('administration/highlighted_brands/', views.HighlightedBrandListView.as_view(), name='highlighted_brand_list'),
    path('administration/highlighted_brands/new/', views.HighlightedBrandCreateView.as_view(), name='highlighted_brand_create'),
    path('administration/highlighted_brands/<int:pk>/edit/', views.HighlightedBrandUpdateView.as_view(), name='highlighted_brand_update'),
    path('administration/highlighted_brands/<int:pk>/delete/', views.HighlightedBrandDeleteView.as_view(), name='highlighted_brand_delete'),
]
