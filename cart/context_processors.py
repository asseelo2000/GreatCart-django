# In Django, context processors are simple Python functions that provide additional context (data) to all your templates. This allows you to make certain variables or data available across multiple templates without having to pass them individually from each view.

from cart.models import CartItme, ShoppingCart
from cart.views import _cart_id


def cart_item_count(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = ShoppingCart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItme.objects.all().filter(user =request.user)
            else:
                cart_items = CartItme.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity 
            # print(cart_count)
        except ShoppingCart.DoesNotExist:
            cart_count = 0  # If the cart doesn't exist, return a count of 0
    return {'cart_count': cart_count}