from django.urls import path
from . import views


urlpatterns = [
    path('administration/categories/list/', views.CategoryListView.as_view(), name='category_list'),
    path('administration/categories/json/', views.category_list_json, name='category_list_json'),
    path('administration/categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('administration/categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('administration/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]
