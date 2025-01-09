from django.urls import path
from . import views

urlpatterns = [
    path('administration/branches/list', views.BranchListView.as_view(), name='branch_list'),
    path('administration/branches/create', views.BranchCreateView.as_view(), name='branch_create'),
    path('administration/branches/<int:pk>/detail', views.BranchDetailView.as_view(), name='branch_detail'),
    path('administration/branches/<int:pk>/update', views.BranchUpdateView.as_view(), name='branch_update'),
]