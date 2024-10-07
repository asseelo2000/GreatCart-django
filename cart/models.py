from django.db import models
from store.models import Product

# Create your models here.

class ShoppingCart(models.Model):
    cart_id = models.CharField(max_length=250, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItme(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.product


