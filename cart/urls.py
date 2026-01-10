"""
Cart URL Configuration
Maps URLs to cart views
"""

from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart detail page
    path('', views.cart_detail, name='cart_detail'),
    
    # Add product to cart
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    
    # Remove product from cart
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    
    # Update product quantity in cart
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
]