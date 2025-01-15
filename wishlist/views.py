from django.shortcuts import render, redirect
from store.models import Product
from django.shortcuts import get_object_or_404
from .models import Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url='my-login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if created:
        # Product was added to wishlist
        messages.success(request, 'Added to your wishlist!')
    else:
        # Product was already in wishlist
        messages.info(request, 'This product is already in your wishlist.')
    return redirect('product_detail', product_id=product_id)