"""
Cart Views
Handles cart display, adding items, removing items, and updating quantities
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart


def cart_detail(request):
    """
    Display cart contents
    """
    cart = Cart(request)
    
    # Calculate totals for template
    for item in cart:
        item['update_quantity_form'] = {
            'quantity': item['quantity'],
            'update': True
        }
    
    context = {'cart': cart}
    return render(request, 'cart/cart_detail.html', context)


@require_POST
def cart_add(request, product_id):
    """
    Add a product to the cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Check stock availability
    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} items available in stock.')
        return redirect('store:product_detail', slug=product.slug)
    
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'{product.name} added to cart.')
    
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """
    Remove a product from the cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'{product.name} removed from cart.')
    
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """
    Update product quantity in cart
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    # Validate quantity against stock
    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} items available in stock.')
        return redirect('cart:cart_detail')
    
    if quantity > 0:
        cart.update_quantity(product_id, quantity)
        messages.success(request, 'Cart updated successfully.')
    else:
        cart.remove(product)
        messages.info(request, f'{product.name} removed from cart.')
    
    return redirect('cart:cart_detail')