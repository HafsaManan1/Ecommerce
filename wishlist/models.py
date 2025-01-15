from django.db import models
from django.contrib.auth.models import User
from store.models import Product

# Create your models here.
class Wishlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    wishlist_item = models.ForeignKey(Product, on_delete=models.CASCADE)

    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}"