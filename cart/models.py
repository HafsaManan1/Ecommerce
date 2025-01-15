from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from store.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    session_key = models.CharField(max_length=40, null=True, blank=True)


