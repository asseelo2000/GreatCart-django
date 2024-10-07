from django.shortcuts import render
from store.models import Product


def home(request):
    # Query all available products (stock_quantity > 0)
    available_products = Product.objects.filter(stock_quantity__gt=0)

    context = {
        "products": available_products,
    }
    # Pass the available products to the template
    return render(request, "home.htm", context)

def signin(request):
    return render(request, "signin.htm")
