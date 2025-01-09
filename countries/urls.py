from django.urls import path
from . import views

urlpatterns = [
    path('administration/country/list', views.CountryListView.as_view(), name='country_list'),
    path('administration/country/create', views.CountryCreateView.as_view(), name='country_create'),
    path('administration/country/<int:pk>/detail', views.CountryDetailView.as_view(), name='country_detail'),
    path('administration/country/<int:pk>/update', views.CountryUpdateView.as_view(), name='country_update'),
]