from django.db import models
from store.models import Product, Variation
from accounts.models import Account

# Create your models here.

class ShoppingCart(models.Model):
    cart_id = models.CharField(max_length=250, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItme(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=1)

    def subtotal(self):
        """Calculate the subtotal for the cart item."""
        return self.product.price * self.quantity
        
    def __unicode__(self):
        return self.product


