from django.urls import path
from . import views

urlpatterns = [
    path('administration/customer_type/', views.CustomerTypeListView.as_view(), name='customer_type_list'),
    path('administration/customer_type/create/', views.CustomerTypeCreateView.as_view(), name='customer_type_create'),
    path('administration/customer_type/<int:pk>/detail/', views.CustomerTypeDetailView.as_view(), name='customer_type_detail'),
    path('administration/customer_type/<int:pk>/update/', views.CustomerTypeUpdateView.as_view(), name='customer_type_update'),

    path('administration/customer_state/', views.CustomerStateListView.as_view(), name='customer_state_list'),
    path('administration/customer_state/create/', views.CustomerStateCreateView.as_view(), name='customer_state_create'),
    path('administration/customer_state/<int:pk>/detail/', views.CustomerStateDetailView.as_view(), name='customer_state_detail'),
    path('administration/customer_state/<int:pk>/update/', views.CustomerStateUpdateView.as_view(), name='customer_state_update'),

    path('administration/customer/', views.CustomerListView.as_view(), name='customer_list'),
    path('administration/customer/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('administration/customer/<int:pk>/detail/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('administration/customer/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer_update'),
]
