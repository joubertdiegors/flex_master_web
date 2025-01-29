from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    
    path('register/', views.RegisterBasicView.as_view(), name='register'),
    path('verify-email/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('complete_registration/<int:customer_id>/', views.CompleteRegistrationView.as_view(), name='complete_registration'),
    path('logout/', views.logout_view, name='logout'),

    # Esqueci a senha
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]