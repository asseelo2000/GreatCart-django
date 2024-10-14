from django.contrib import admin
from .models import ShoppingCart, CartItme

# Register your models here.
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')

admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(CartItme, CartItemAdmin)