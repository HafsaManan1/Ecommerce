from django.shortcuts import render, redirect
from . models import Category, Product, ReviewRating, Wishlist
from payment.models import OrderItem
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
def store(request):
    all_products = Product.objects.all()
    user = request.user
    wishlist_product_ids = []
    latest_products = Product.objects.order_by('-id')[:5]
    is_first_purchase = False
    if user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(user=user).values_list('product_id', flat=True)
        is_first_purchase = not user.order_set.exists() 
    context = {'my_products': all_products, 'show_navbar': True,'wishlist_product_ids': wishlist_product_ids, 'latest_products': latest_products, 'is_first_purchase' : is_first_purchase}
    return render(request, 'store/store.html', context)

def categories(request):
    all_categories = Category.objects.all()
    wishlist_product_ids = []
    user = request.user
    if user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(user=user).values_list('product_id', flat=True)
    return {'all_categories': all_categories, 'show_navbar': True, 'wishlist_product_ids': wishlist_product_ids}

def product_info(request,product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    user = request.user
    can_review = False
    review_exists = False
    product_in_wishlist = False

    if user.is_authenticated:
        can_review = OrderItem.objects.filter(user=user, product=product).exists()
        review_exists = ReviewRating.objects.filter(user=user, product=product).exists()
        product_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        

    reviews = ReviewRating.objects.filter(product=product).order_by('-created_date')
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:6]

    context = {'product':product, 'can_review': can_review, 'reviews': reviews, 'review_exists': review_exists, 'product_in_wishlist': product_in_wishlist, 'show_navbar': True, 'rating_range': range(1, 6), 'related_products':related_products}
    return render(request,'store/product-info.html', context)

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html',{'category' : category, 'products' : products})

def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    if request.method == 'POST':
        review_text = request.POST.get('review', '')
        ratings = request.POST.get('ratings', 0)
        image = request.FILES.get('image') 

        if OrderItem.objects.filter(user=user, product=product).exists():
            
            review = ReviewRating(
                product=product,
                user=user,
                review=review_text,
                ratings=ratings,
                image=image,  
            )
            review.save()
        

        return redirect('product-info', product_slug=product.slug)
    
    return redirect('product-info', product_slug=product.slug)

def toggle_wishlist(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please Login to add this item to wishlist.')
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            return JsonResponse({'added': True})
        else:
            wishlist_item.delete()
            return JsonResponse({'added': False})
        

@login_required(login_url='my-login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, SearchHeadline
from django.shortcuts import render
from .models import Product

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        search_vector = SearchVector('title', 'description')
        search_query = SearchQuery(query)
        search_headline = SearchHeadline('description', search_query)
        results = Product.objects.annotate(rank=SearchRank(search_vector, search_query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')

    wishlist_product_ids = []
    user = request.user
    if user.is_authenticated:
        wishlist_product_ids = Wishlist.objects.filter(user=user).values_list('product_id', flat=True)
    return render(request, 'store/search_results.html', {'query': query, 'results': results, 'wishlist_product_ids': wishlist_product_ids})

def about_us(request):
    context = {'show_navbar': True}
    return render(request, 'store/about-us.html', context)\
    
def terms_conditions(request):
    context = {'show_navbar': True}
    return render(request, 'store/terms-conditions.html', context)

def faq(request):
    context = {'show_navbar': True}
    return render(request, 'store/faq.html', context)

def privacy_policy(request):
    context = {'show_navbar': True}
    return render(request, 'store/privacy-policy.html', context)

def delivery_information(request):
    context = {'show_navbar': True}
    return render(request, 'store/delivery-information.html', context)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"Message from {name} ({email}):\n\n{message}"
        try:
            email_message = EmailMessage(
                subject=subject,
                body=full_message,
                from_email=settings.EMAIL_HOST_USER,  
                to=[settings.CONTACT_EMAIL],                  
            )
            print(email_message)
            email_message.send()

            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "There was an error sending your message. Please try again later.")
        
        return redirect("contact")  

    return render(request, "store/contact.html")
