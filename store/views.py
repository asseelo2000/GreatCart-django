from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from cart.models import CartItme, ShoppingCart
from cart.views import _cart_id
from store.models import Product, Category


# Create your views here.


def store(request, category_slug=None):
    # If a category slug is provided, filter products by that category
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_avaliable=True
        )  # Filter products by the selected category

        # Set up the paginator for each category
        paginator = Paginator(products, 1)  # Show 1 products per page
        page = request.GET.get('page')  # Get the page number from the URL
        paged_products = paginator.get_page(page)  # Get the products for that page
        products_count = products.count()
    else:
        # Query all available products (stock_quantity > 0)
        products = Product.objects.all().filter(stock_quantity__gt=0).order_by('id') # orderd for consistent pagination
        products_count = products.count()

        # Set up the paginator for all products
        paginator = Paginator(products, 6)  # Show 6 products per page
        page = request.GET.get('page')  # Get the page number from the URL
        paged_products = paginator.get_page(page)  # Get the products for that page

    context = {
        "products": paged_products,
        "products_count": products_count,
    }
    return render(request, "store/store.htm", context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug
        )
    except Exception as e:
        raise e

    in_cart = False

    # Check if the product is in the user's cart
    try:
        cart = ShoppingCart.objects.get(cart_id=_cart_id(request))
        if CartItme.objects.filter(product=single_product, cart=cart).exists():
            in_cart = True
    except ShoppingCart.DoesNotExist:
        pass  # If the cart doesn't exist, the product can't be in the cart
    context = {
        "single_product": single_product,
        "in_cart": in_cart,  # Pass the flag to the template
    }

    return render(request, "store/product-details.htm", context)

def search(request):
    products = Product.objects.all().order_by('id')  # Default ordering
    # Get the search term from the GET request
    search_query = request.GET.get('keyword')
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | Q(description__icontains=search_query)
        )  # Search in product name and description fields

    #  pagination
    paginator = Paginator(products, 6)  # Show 6 products per page
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    products_count = products.count()
    
    context = {
        'products': paged_products,
        'search_query': search_query,
        'products_count':products_count,
    }
    return render(request, 'store/store.htm', context)

