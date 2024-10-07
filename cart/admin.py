from django.contrib import admin
from .models import ShoppingCart, CartItme

# Register your models here.

admin.site.register(ShoppingCart)
admin.site.register(CartItme)