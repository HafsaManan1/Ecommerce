from store.models import Product
from decimal import Decimal
from .models import CartItem
import copy

class Cart():
    def __init__(self, request):
        self.request = request
        self.user = request.user if request.user.is_authenticated else None
        self.session = request.session

        if self.user:
            self.cart = CartItem.objects.filter(user=self.user)
        else:
            # Use 'cart' session key to store guest cart items
            self.cart = self.session.get('cart', {})

    def add(self, product, product_qty):
        product_id = str(product.id)

        if self.user:
            # Update or create cart item for authenticated user
            CartItem.objects.update_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': product_qty}
            )
        else:
            # Update or add new product to session cart for guest user
            if product_id in self.cart:
                self.cart[product_id]['qty'] = product_qty
            else:
                self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

            # Save cart back to the session
            self.session['cart'] = self.cart
            self.session.modified = True

    def __len__(self):
        if self.user:
            return sum(item.quantity for item in self.cart)
        else:
            return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        if self.user:
            # For authenticated users
            all_product_ids = [item.product.id for item in self.cart]
            products = Product.objects.filter(id__in=all_product_ids)
            cart = copy.deepcopy(self.cart)

            for item in self.cart:
                product = products.get(id=item.product.id)
                yield {
                    'product': product,
                    'quantity': item.quantity,
                    'price': Decimal(product.price),
                    'total': Decimal(product.price) * item.quantity,
                }

        else:
            # For guest users (session-based cart)
            all_product_ids = self.cart.keys()
            products = Product.objects.filter(id__in=all_product_ids)
            cart = copy.deepcopy(self.cart)

            for product in products:
                cart_item = cart[str(product.id)]
                yield {
                    'product': product,
                    'quantity': cart_item['qty'],
                    'price': Decimal(cart_item['price']),
                    'total': Decimal(cart_item['price']) * cart_item['qty'],
                }


    def get_total(self):
        total = 0
        if self.user:
            total = sum(Decimal(item.product.price) * item.quantity for item in self.cart)
        else:
            total = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
        
        if self.user and not self.user.order_set.exists():  
            total *= Decimal(0.75) 

        return total

    # def get_total(self):
    #     total_price = 0
    #     discounted_price = 0
    #     is_discount_applied = False

    #     if self.user:
    #         total_price = sum(Decimal(item.product.price) * item.quantity for item in self.cart)
    #         if not self.user.order_set.exists():  # Check for first purchase
    #             discounted_price = total_price * Decimal(0.75)
    #             is_discount_applied = True
    #         else:
    #             discounted_price = total_price
    #     else:
    #         total_price = sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
    #         discounted_price = total_price  # No discount for guest users

    #     return {
    #         'total_price': total_price,
    #         'discounted_price': discounted_price,
    #         'is_discount_applied': is_discount_applied,
    #     }


    def delete(self, product):
        product_id = str(product)

        if self.user:
            # Remove item from database cart for authenticated user
            CartItem.objects.filter(user=self.user, product=product).delete()
        else:
            # Remove item from session-based cart for guest user
            if product_id in self.cart:
                del self.cart[product_id]
                # Update session
                self.session['cart'] = self.cart
                self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)

        if self.user:
            cart_item = CartItem.objects.filter(user=self.user, product=product).first()
            if cart_item:
                cart_item.quantity = qty
                cart_item.save()
        else:
            if product_id in self.cart:
                self.cart[product_id]['qty'] = qty
                # Update session
                self.session['cart'] = self.cart
                self.session.modified = True

    def clear(self):
        if self.user:
            # Clear all items from the database cart for authenticated user
            CartItem.objects.filter(user=self.user).delete()
        else:
            # Clear all items from session-based cart for guest users
            self.session['cart'] = {}
            self.session.modified = True

    def merge_cart_on_login(self):
        if self.user and 'cart' in self.session:
            session_cart = self.session['cart']  # Correctly fetch the guest cart data

            for product_id, data in session_cart.items():
                product = Product.objects.get(id=product_id)
                CartItem.objects.update_or_create(
                    user=self.user,
                    product=product,
                    defaults={'quantity': data['qty']}
                )

            # Clear guest cart from session after merge
            del self.session['cart']
            self.session.modified = True