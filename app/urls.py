from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from .views import home

from django.views.generic import RedirectView

from django.conf.urls import handler404
from .views import custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('accounts.urls')),
    path('dashboard/', home, name='dashboard'),

    path('', include('branches.urls')),
    path('', include('cart.urls')),
    path('', include('countries.urls')),
    path('', include('customers.urls')),
    path('', include('purchases.urls')),
    path('', include('suppliers.urls')),
    path('', include('categories.urls')),
    path('', include('products.urls')),
    path('', include('promotions.urls')),

    path('', include('store.urls')),
    path('', include('customization_store.urls')),

    path('favicon.ico', RedirectView.as_view(url=settings.MEDIA_URL + 'logos/favicon.ico')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configuração da view personalizada para erros 404
handler404 = custom_page_not_found_view
