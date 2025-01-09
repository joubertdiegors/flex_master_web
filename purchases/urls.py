from django.urls import path
from . import views

urlpatterns = [
    path('supplier-product-price/list', views.SupplierProductPriceListView.as_view(), name='supplier_product_price_list'),
    path('supplier-product-price/create', views.SupplierProductPriceCreateView.as_view(), name='supplier_product_price_create'),
    path('supplier-product-price/<int:pk>/detail', views.SupplierProductPriceDetailView.as_view(), name='supplier_product_price_detail'),
    path('supplier-product-price/<int:pk>/update', views.SupplierProductPriceUpdateView.as_view(), name='supplier_product_price_update'),

    path('purchase-orders/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase-order/new/', views.PurchaseOrderCreateView.as_view(), name='purchase_order_create'),
    path('purchase-order/<int:pk>/edit/', views.PurchaseOrderUpdateView.as_view(), name='purchase_order_update'),
    path('purchase-order/<int:pk>/delete/', views.PurchaseOrderDeleteView.as_view(), name='purchase_order_delete'),
    
    # Busca do preço de compra com base no fornecedor e produto.
    path('get-product-price/', views.get_product_price, name='get_product_price'),
]
