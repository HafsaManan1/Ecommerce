from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name='store'),
    #individual product
    path('product/<slug:product_slug>/', views.product_info, name='product-info'),
    #individual category
    path('search/<slug:category_slug>/', views.list_category, name='list-category'),

    path('submit-review/<int:product_id>/', views.submit_review, name='submit-review'),

    path('wishlist/', views.wishlist_view, name='wishlist'),
    
    path('toggle-wishlist/', views.toggle_wishlist, name='toggle-wishlist'),

    path('search/', views.search, name='search'),
    path('about-us/', views.about_us, name='about-us'),
    path('terms-and-conditions/', views.terms_conditions, name='terms-and-conditions'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('delivery-information/', views.delivery_information, name='delivery-information'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
]