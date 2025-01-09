from django.urls import path
from . import views

urlpatterns = [
    path('administration/promotions/', views.PromotionListView.as_view(), name='promotion_list'),
    path('administration/promotions/create/', views.PromotionCreateView.as_view(), name='promotion_create'),
    path('administration/promotions/<int:pk>/', views.PromotionDetailView.as_view(), name='promotion_detail'),
    path('administration/promotions/<int:pk>/update/', views.PromotionUpdateView.as_view(), name='promotion_update'),
    path('administration/promotions/<int:pk>/delete/', views.PromotionDeleteView.as_view(), name='promotion_delete'),
]