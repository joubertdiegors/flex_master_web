from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register/', views.RegisterBasicView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate_email, name='activate'),
    path('resend_verification/<int:customer_id>/', views.resend_verification, name='resend_verification'),
    path('email_confirmation_sent/<str:email>/', views.EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),

    path('complete_registration/<int:customer_id>/', views.CompleteRegistrationView.as_view(), name='complete_registration'),
    path('logout/', views.logout_view, name='logout'),

    # Esqueci a senha
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]