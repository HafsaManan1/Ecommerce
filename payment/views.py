from django.shortcuts import render

from . models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.conf import settings

import stripe

from django.http import JsonResponse
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def payment_success(request):
    # Clear the shopping cart
    cart = Cart(request)
    # Clear the shopping cart after payment is successful
    cart.clear()
    # for key in list(request.session.keys()):
        
    #     if key == 'session_key':

    #         del request.session[key]
    
    return render(request, 'payment/payment-success.html')

def payment_failed(request):
    return render(request, 'payment/payment-failed.html')

def checkout(request):
    #prefilled for logged in code
    if request.user.is_authenticated:
        try:
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address, 'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'show_navbar': True}
            return render(request, 'payment/checkout.html', context=context)

        except:
            #authenticated users with no shipping address
            context = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'show_navbar': True}
            return render(request, 'payment/checkout.html', context=context)
        
    else:
        context = {'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY, 'show_navbar': True}
        return render(request, 'payment/checkout.html', context=context)
    
def complete_order(request):

    if request.POST.get('action') == 'post':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # All in one shipping address

        shipping_address = (address1 + "\n" + address2 + "\n" + city + "\n" + state + "\n" + zipcode)
        # Shopping cart information
        cart = Cart(request)
        total_cost = cart.get_total()

        '''
        Order Variations:

        1) Create order --> Account users WITH + WITHOUT shipping information

        2) Create order --> Guest users without an account

        '''

        # 1) Create order --> Account users WITH + WITHOUT shipping information

        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid = total_cost, user=request.user)
            order_id = order.pk
            # final_price = order.calculate_discounted_price()
            # order.amount_paid = final_price
            order.save()
            for item in cart:

                OrderItem.objects.create(order_id = order_id, product = item['product'], quantity = item['quantity'], price = item['price'], user=request.user )

        # 2) Create order --> Guest users without an account

        else:
            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, amount_paid = total_cost)
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(order_id = order_id, product = item['product'], quantity = item['quantity'], price = item['price'])

        order_success = True
        response = JsonResponse({'success': order_success})
        return response

def create_checkout_session(request):
    if request.method == 'POST':
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Total Order',
                        },
                        'unit_amount': int(Cart(request).get_total() * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
    
                success_url=settings.PAYMENT_SUCCESS_URL,
                cancel_url=settings.PAYMENT_CANCEL_URL,
            )
            return JsonResponse({'id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

