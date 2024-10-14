from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, redirect, render
from .models import ShoppingCart, CartItme
from store.models import Product, Variation
from django.http import HttpResponse, HttpResponseRedirect


# Function to get the cart or create one if it doesn't exist, it is private by adding the "_" at the start of the function
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()  # Create a new session if none exists
    return cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # get the product
    product_variations = []

    # Get selected variations (color and size) from the request
    if request.method == "POST":
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variations.append(variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart = ShoppingCart.objects.get(cart_id=_cart_id(request))
    except ShoppingCart.DoesNotExist:
        cart = ShoppingCart.objects.create(cart_id=_cart_id(request))
    cart.save()

    # Check if the cart item with the same product and variations already exists
    cart_items = CartItme.objects.filter(product=product, cart=cart)
    
    # List of existing variations for each cart item
    existing_variations_list = []
    cart_item_ids = []
    for item in cart_items:
        existing_variations = list(item.variations.all())
        existing_variations_list.append(existing_variations)
        cart_item_ids.append(item.id)

    # If the product with the same variations exists, increase quantity
    if product_variations in existing_variations_list:
        index = existing_variations_list.index(product_variations)
        cart_item = CartItme.objects.get(id=cart_item_ids[index])
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If no matching cart item, create a new one
        cart_item = CartItme.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variations) > 0:
            cart_item.variations.add(*product_variations)
        cart_item.save()

    return redirect("cart")  # Redirect to the cart page


def decrease_item_quantity(request, product_id, cart_item_id):
    """Remove a specific product from the cart."""
    cart = ShoppingCart.objects.get(cart_id=_cart_id(request))  # Get the cart using session id
    product = get_object_or_404(Product, id=product_id)  # Get the product
    try:
        cart_item = CartItme.objects.get( product=product, cart=cart, id= cart_item_id)  # Get the cart item to be removed
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # decrease an item from the total item quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove the item from the cart
    except:
        pass

    return redirect("cart")  # Redirect back to the cart page


def remove_from_cart(request, product_id, cart_item_id):
    cart = ShoppingCart.objects.get(cart_id=_cart_id(request))  # Get the cart using session id
    product = get_object_or_404(Product, id=product_id)  # Get the product
    cart_item = CartItme.objects.get(product=product, cart=cart, id= cart_item_id)  # Get the cart item to be removed
    try:
        cart_item.delete()
    except CartItme.DoesNotExist:
        pass
    return redirect("cart")


# Display the cart_item with its details in the cart page
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = ShoppingCart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItme.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax

    except ShoppingCart.DoesNotExist:
        pass  # If the cart does not exist, pass, and the template will handle an empty cart(means ignore)

    context = {
        "cart_items": cart_items,
        "total": total,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "store/cart.htm", context)
