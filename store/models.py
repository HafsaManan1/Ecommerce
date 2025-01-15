from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.
class Category(models.Model):
    # index to speedup the lookups
    name = models.CharField(max_length=250, db_index=True) #db_index=True makes an index of the field for which it is defined. it is just like a index of the book that helps you look up stuff quickly
    slug = models.SlugField(max_length=250, unique=True) #slug is there to ensure uniqueness 
    icon = models.ImageField(upload_to='images/', null=True)

    class Meta:
        verbose_name_plural =  'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('list-category', args=[self.slug])

#slugs are there to define unique category and unique products e.g we can have two same categories and two same products  

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=250, default='un-branded')
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='images/')

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):

        return reverse('product-info', args=[self.slug])
    
    def get_average_rating(self):
        average = self.reviewrating_set.filter(status=True).aggregate(average_rating=Avg('ratings'))['average_rating']
        return round(average, 2) if average else 'No Rating'
    
    def get_ratings_count(self):
        count = self.reviewrating_set.filter(status=True).count()
        return count
    

class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    ratings = models.FloatField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name_plural =  'Reviews&Ratings'

        # unique_together = ('product', 'user')  # Ensure unique user-product review pair

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_user')  # Changed related_name
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_products')  # Changed related_name
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"









    
    

