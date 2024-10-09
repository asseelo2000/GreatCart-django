# In Django, context processors are simple Python functions that provide additional context (data) to all your templates. This allows you to make certain variables or data available across multiple templates without having to pass them individually from each view.

from cart.models import CartItme, ShoppingCart
from cart.views import _cart_id


def cart_item_count(request):
    cart_count = 0
    try:
        cart = ShoppingCart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItme.objects.filter(cart=cart, is_active=True)
        cart_count = sum(item.quantity for item in cart_items)
    except ShoppingCart.DoesNotExist:
        cart_count = 0  # If the cart doesn't exist, return a count of 0
    return {'cart_count': cart_count}