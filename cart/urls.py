from django.urls import path
from . import views

urlpatterns = [  
    path('',views.cart, name= 'cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add item to cart
    path('decrease/<int:product_id>/', views.decrease_item_quantity, name='decrease_item_quantity'),  # remove one item from quantity    
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),  # remove an item from cart

]