"""
Store URL Configuration
Maps URLs to views for the store app
"""

from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Product listing
    path('products/', views.product_list, name='product_list'),
    
    # Product detail
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Category products
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    
    # Search
    path('search/', views.search, name='search'),
]