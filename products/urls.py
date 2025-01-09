from django.urls import path
from . import views

urlpatterns = [
    path('administration/products/', views.ProductListView.as_view(), name='product_list'),
    path('administration/products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('administration/products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('administration/products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('administration/products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('api/products/search/', views.product_search, name='product_search'),

    path('administration/products/ingredients/<int:pk>/', views.IngredientsCreateView.as_view(), name='ingredients_create'),

    path('administration/products/nutritionalitems/', views.NutritionalItemListView.as_view(), name='nutritional_item_list'),
    path('administration/products/nutritionalitems/new/', views.NutritionalItemCreateView.as_view(), name='nutritional_item_create'),
    path('administration/products/nutritionalitems/<int:pk>/edit/', views.NutritionalItemUpdateView.as_view(), name='nutritional_item_update'),
    path('administration/products/nutritionalitems/<int:pk>/delete/', views.NutritionalItemDeleteView.as_view(), name='nutritional_item_delete'),

    path('administration/products/nutritionalinfo/<int:pk>', views.NutritionalInfoView.as_view(), name='nutritional_info_create'),
    path('administration/products/nutritionalinfo/delete/<int:pk>/', views.NutritionalInfoDeleteView.as_view(), name='nutritional_info_delete'),

    path('administration/brands/', views.BrandListView.as_view(), name='brand_list'),
    path('administration/brands/create/', views.BrandCreateView.as_view(), name='brand_create'),
    path('administration/brands/<int:pk>/', views.BrandDetailView.as_view(), name='brand_detail'),
    path('administration/brands/<int:pk>/update/', views.BrandUpdateView.as_view(), name='brand_update'),
    path('administration/brands/<int:pk>/delete/', views.BrandDeleteView.as_view(), name='brand_delete'),

    path('administration/sales_unit/', views.SalesUnitListView.as_view(), name='sales_unit_list'),
    path('administration/sales_unit/create/', views.SalesUnitCreateView.as_view(), name='sales_unit_create'),
    path('administration/sales_unit/<int:pk>/', views.SalesUnitDetailView.as_view(), name='sales_unit_detail'),
    path('administration/sales_unit/<int:pk>/update/', views.SalesUnitUpdateView.as_view(), name='sales_unit_update'),
    path('administration/sales_unit/<int:pk>/delete/', views.SalesUnitDeleteView.as_view(), name='sales_unit_delete'),

    path('administration/package_unit/', views.PackageUnitListView.as_view(), name='package_unit_list'),
    path('administration/package_unit/create/', views.PackageUnitCreateView.as_view(), name='package_unit_create'),
    path('administration/package_unit/<int:pk>/', views.PackageUnitDetailView.as_view(), name='package_unit_detail'),
    path('administration/package_unit/<int:pk>/update/', views.PackageUnitUpdateView.as_view(), name='package_unit_update'),
    path('administration/package_unit/<int:pk>/delete/', views.PackageUnitDeleteView.as_view(), name='package_unit_delete'),

]
