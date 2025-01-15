from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register', views.register, name='register'),

    #Email verification URL's
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),

    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),

    path('email-verification-success', views.email_verification_success, name='email-verification-success'),

    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),

    # Login / Logout functionality

    path('my-login', views.my_login, name='my-login'),

    path('user-logout', views.user_logout, name='user-logout'),

    # Dashboard / Profile urls

    path('dashboard', views.dashboard, name='dashboard'),

    path('profile-management', views.profile_management, name='profile-management'),

    path('delete-account', views.delete_account, name='delete-account'),

    # Password Management urls/views

    # 1) Submit our email form

    path('reset_password', views.CustomPasswordResetView.as_view(), name='reset_password'),

    # 2) Success message stating that a password reset email was sent

    path('reset_password_sent', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),

    # 3) Password reset link

    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # 4) Success message stating that our  password was reset

    path('reset_password_complete', views.CustomPasswordResetCompleteView.as_view(template_name='account/password/password-reset-complete.html'), name='password_reset_complete'),

    # Manage shipping

    path('manage-shipping', views.manage_shipping, name='manage-shipping'),

    path('track-orders', views.track_orders, name='track-orders'),
 
    
]