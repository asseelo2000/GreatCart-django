from django.shortcuts import get_object_or_404, render
from store.models import Product, Category

# Create your views here.


def store(request, category_slug=None):
    # If a category slug is provided, filter products by that category
    products = None

    
    if category_slug!=None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_avaliable = True)  # Filter products by the selected category
        products_count = products.count()
    else:
        # Query all available products (stock_quantity > 0)
        products = Product.objects.all().filter(stock_quantity__gt=0)
        products_count = products.count()
    
    context = {
        "products": products,
        "products_count": products_count,
    }
    return render(request, "store/store.htm",context)

def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e: 
        raise e
    
    context = {
        'single_product': single_product,
    }

    return render(request, 'store/product-details.htm', context)   

