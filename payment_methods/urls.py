from django.urls import path
from . import views

urlpatterns = [
    path("payment-methods/", views.PaymentMethodListView.as_view(), name="payment_method_list"),
    path("payment-methods/create/", views.PaymentMethodCreateView.as_view(), name="payment_method_create"),
    path("payment-methods/<int:pk>/", views.PaymentMethodDetailView.as_view(), name="payment_method_detail"),
    path("payment-methods/<int:pk>/update/", views.PaymentMethodUpdateView.as_view(), name="payment_method_update"),
    path("payment-methods/<int:pk>/delete/", views.PaymentMethodDeleteView.as_view(), name="payment_method_delete"),

    # PDV API continua aqui:
    path("api/pdv/sync/payment-methods/", views.pdv_payment_methods_sync, name="pdv_payment_methods_sync"),
]
