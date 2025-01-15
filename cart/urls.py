from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_summary, name='cart-summary'),
    #cart add functionality
    path('add/', views.cart_add, name='cart-add'),
    #cart updation functionality
    path('update/', views.cart_update, name='cart-update'),
    #cart deletion functionality
    path('delete/', views.cart_delete, name='cart-delete'),
    path('cart-partial/', views.cart_partial, name='cart-partial')
]