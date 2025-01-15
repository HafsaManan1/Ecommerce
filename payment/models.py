from django.db import models

from django.contrib.auth.models import User

from store.models import Product

from decimal import Decimal

# Create your models here.

# This whole form is optionl

class ShippingAddress(models.Model):

    full_name =  models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    # Optional things
    state = models.CharField(max_length=255, null=True, blank=True) #null=True for database and blank=True is for client side that this field is not compulsary
    zipcode = models.CharField(max_length=255, null=True, blank=True)
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return 'Shipping Address - ' + str(self.id)
    
class Order(models.Model):
    full_name =  models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=10000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_order = models.DateTimeField(auto_now_add=True)
    # FK
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return 'Order - #' + str(self.id) +  ' ' +str(self.full_name) + ' ' + str(self.email)
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #null=True for database and blank=True is for client side that this field is not compulsary - for guest user

    def __str__(self):
        return 'Order Item : ' + str(self.id) + ' Product : ' + str(self.product) + ' Quantity : ' +  str(self.quantity) + ' Price : ' + str(self.price)
