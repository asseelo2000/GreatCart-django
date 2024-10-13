from django.db import models
from django.urls import reverse
from category.models import Category
from django.db.models import CheckConstraint, Q

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length= 400, blank= True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to= 'photos/products', blank= True)
    stock_quantity = models.IntegerField(default=0)
    is_avaliable = models.BooleanField(default= True)
    created_at = models.DateTimeField(auto_now_add= True)
    modified_at = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse('product_details', args=[self.category.slug, self.slug])
    

class Variation(models.Model):
    VARIATION_CATEGORY_CHOICES = (
        ('color', 'Color'),
        ('size', 'Size'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=VARIATION_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variation_value} ({self.variation_category})" 