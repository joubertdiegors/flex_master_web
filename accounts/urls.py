from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterBasicView.as_view(), name='register'),
    path('complete_registration/<int:customer_id>/', views.CompleteRegistrationView.as_view(), name='complete_registration'),
    path('gestao', views.login_view, name='gestao'),
    path('logout/', views.logout_view, name='logout'),
]