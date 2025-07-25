from django.urls import path
from . import views
from .views_flush import flush_pdv_data

urlpatterns = [
    path('pdv/flush/', flush_pdv_data, name='flush_pdv_data'),
    
    path("api/pdv/cash/open-status/", views.get_open_cash_status, name="pdv_cash_open_status"),
    path("api/pdv/cash/list/", views.list_cash_registers, name="pdv_cash_list"),
    path("api/pdv/cash/open/", views.pdv_open_cash, name="pdv_cash_open"),
    path("api/pdv/cash/close/", views.pdv_close_cash, name="pdv_cash_close"),
    path("api/pdv/cash/history/", views.pdv_cash_history, name="pdv_cash_history"),
    path('cash-register/history/', views.CashRegisterHistoryView.as_view(), name='cash_register_history'),

    # CRUD de favoritos
    path("favorites/", views.FavoriteProductListView.as_view(), name="favorite_list"),
    path("favorites/create/", views.FavoriteProductCreateView.as_view(), name="favorite_create"),
    path("favorites/<int:pk>/", views.FavoriteProductDetailView.as_view(), name="favorite_detail"),
    path("favorites/<int:pk>/update/", views.FavoriteProductUpdateView.as_view(), name="favorite_update"),
    path("favorites/<int:pk>/delete/", views.FavoriteProductDeleteView.as_view(), name="favorite_delete"),

    # Tela de tickets de venda pelo PDV
    path("sales/", views.PdvSaleListView.as_view(), name="pdv_sale_list"),
    path("pdv/sales/<uuid:pk>/", views.PdvSaleDetailView.as_view(), name="pdvsale_detail"),

    # Produtos favoritos no PDV
    path("api/pdv/sync/favorites/", views.pdv_favorite_list, name="pdv_favorite_list"),

    # vendas do PDV
    path("api/pdv/sales/list/", views.pdv_sales_list, name="pdv_sales_list"),
    path("api/pdv/sales/create/", views.pdv_sale_create, name="pdv_sale_create"),

    # Compras em espera do PDV
    path("api/pdv/hold/create/", views.pdv_hold_create, name="pdv_hold_create"),
    path("api/pdv/hold/list/", views.pdv_hold_list, name="pdv_hold_list"),
    path("api/pdv/hold/delete/<uuid:hold_id>/", views.pdv_hold_delete, name="pdv_hold_delete"),
]
