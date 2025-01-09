from django.urls import path
from . import views

urlpatterns = [
    path('administration/supplier_type/', views.SupplierTypeListView.as_view(), name='supplier_type_list'),
    path('administration/supplier_type/create/', views.SupplierTypeCreateView.as_view(), name='supplier_type_create'),
    path('administration/supplier_type/<int:pk>/detail/', views.SupplierTypeDetailView.as_view(), name='supplier_type_detail'),
    path('administration/supplier_type/<int:pk>/update/', views.SupplierTypeUpdateView.as_view(), name='supplier_type_update'),

    path('administration/supplier_state/', views.SupplierStateListView.as_view(), name='supplier_state_list'),
    path('administration/supplier_state/create/', views.SupplierStateCreateView.as_view(), name='supplier_state_create'),
    path('administration/supplier_state/<int:pk>/detail/', views.SupplierStateDetailView.as_view(), name='supplier_state_detail'),
    path('administration/supplier_state/<int:pk>/update/', views.SupplierStateUpdateView.as_view(), name='supplier_state_update'),

    path('administration/supplier/', views.SupplierListView.as_view(), name='supplier_list'),
    path('administration/supplier/create/', views.SupplierCreateView.as_view(), name='supplier_create'),
    path('administration/supplier/<int:pk>/detail/', views.SupplierDetailView.as_view(), name='supplier_detail'),
    path('administration/supplier/<int:pk>/update/', views.SupplierUpdateView.as_view(), name='supplier_update'),
]
