from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, redirect, render
from .models import ShoppingCart, CartItme
from store.models import Product
from django.http import HttpResponse, HttpResponseRedirect


# Function to get the cart or create one if it doesn't exist, it is private by adding the "_" at the start of the function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()  # Create a new session if none exists
    return cart


# Add a product to the cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # get the product
    try:
        cart = ShoppingCart.objects.get(
            cart_id=_cart_id(request)
        )  # get the cart from the cart_id present in the session
    except ShoppingCart.DoesNotExist:
        cart = ShoppingCart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        # Check if the item already exists in the cart, if not then create one
        cart_item = CartItme.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # If the item exists, increment the quantity
        cart_item.save()
    except CartItme.DoesNotExist:
        cart_item = CartItme.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()
    
    return redirect("cart")  # Redirect to the cart page

def decrease_item_quantity(request, product_id):
    """Remove a specific product from the cart."""
    cart = ShoppingCart.objects.get(cart_id=_cart_id(request))  # Get the cart using session id
    product = get_object_or_404(Product, id=product_id)  # Get the product
    cart_item = CartItme.objects.get(product=product, cart=cart)     # Get the cart item to be removed
 
    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # decrease an item from the total item quantity
        cart_item.save()
    else:
        cart_item.delete()  # Remove the item from the cart
    
    return redirect('cart')  # Redirect back to the cart page

def remove_from_cart(request, product_id):
    cart = ShoppingCart.objects.get(cart_id=_cart_id(request))  # Get the cart using session id
    product = get_object_or_404(Product, id=product_id)  # Get the product
    cart_item = CartItme.objects.get(product=product, cart=cart)     # Get the cart item to be removed
    try:
        cart_item.delete()
    except CartItme.DoesNotExist:
        pass 
    return redirect("cart")
# Display the cart_item with its details in the cart page
def cart(request,total = 0, quantity = 0, cart_items = None ): 
    try:
        cart = ShoppingCart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItme.objects.filter(cart=cart, is_active=True)
        
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ShoppingCart.DoesNotExist:
        pass  # If the cart does not exist, pass, and the template will handle an empty cart(means ignore)

    context = {
        'cart_items': cart_items,
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.htm', context)
