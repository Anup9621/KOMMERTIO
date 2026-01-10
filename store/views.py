"""
Store Views
Handles home page, product listing, product detail, search, and category filtering
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product, Category


def home(request):
    """
    Home page view with featured products and categories
    """
    featured_products = Product.objects.filter(
        featured=True, 
        available=True
    )[:8]
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)


def product_list(request):
    """
    Display all available products with pagination
    """
    products = Product.objects.filter(available=True)
    
    # Pagination - 12 products per page
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'page_title': 'All Products',
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """
    Display individual product details
    """
    product = get_object_or_404(
        Product, 
        slug=slug, 
        available=True
    )
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def category_products(request, slug):
    """
    Display products filtered by category
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(
        category=category, 
        available=True
    )
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'products': products,
        'page_title': f'{category.name} Products',
    }
    return render(request, 'store/product_list.html', context)


def search(request):
    """
    Search products by name or description
    """
    query = request.GET.get('q', '')
    products = Product.objects.none()
    
    if query:
        # Search in product name and description
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            available=True
        ).distinct()
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'query': query,
        'page_title': f'Search Results for "{query}"' if query else 'Search',
    }
    return render(request, 'store/search_results.html', context)