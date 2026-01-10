"""
Orders Views
Handles checkout process, payment, and order history
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm
import stripe

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    """
    Checkout page with shipping address form
    """
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Store order ID in session for payment
            request.session['order_id'] = order.id
            
            # Redirect to payment
            return redirect('orders:payment')
    else:
        form = OrderCreateForm(user=request.user)
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def payment(request):
    """
    Payment page with Stripe integration
    """
    order_id = request.session.get('order_id')
    
    if not order_id:
        messages.error(request, 'No order found.')
        return redirect('cart:cart_detail')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Get Stripe token from form
        token = request.POST.get('stripeToken')
        
        try:
            # Create Stripe charge
            charge = stripe.Charge.create(
                amount=int(order.total_amount * 100),  # Convert to cents
                currency='usd',
                description=f'Order #{order.id}',
                source=token,
            )
            
            # Update order with payment details
            order.payment_status = 'completed'
            order.payment_id = charge.id
            order.status = 'processing'
            order.save()
            
            # Update product stock
            for item in order.items.all():
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            # Clear the cart
            cart = Cart(request)
            cart.clear()
            
            # Clear order ID from session
            del request.session['order_id']
            
            messages.success(request, 'Payment successful! Your order has been placed.')
            return redirect('orders:payment_success', order_id=order.id)
            
        except stripe.error.CardError as e:
            # Card was declined
            messages.error(request, f'Payment failed: {e.user_message}')
            order.payment_status = 'failed'
            order.save()
            return redirect('orders:payment_failed')
        
        except Exception as e:
            # Something else happened
            messages.error(request, 'An error occurred during payment.')
            order.payment_status = 'failed'
            order.save()
            return redirect('orders:payment_failed')
    
    context = {
        'order': order,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'orders/payment.html', context)


@login_required
def payment_success(request, order_id):
    """
    Payment success confirmation page
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {'order': order}
    return render(request, 'orders/payment_success.html', context)


@login_required
def payment_failed(request):
    """
    Payment failure page
    """
    return render(request, 'orders/payment_failed.html')


@login_required
def order_history(request):
    """
    Display user's order history
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    
    context = {'orders': orders}
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail(request, order_id):
    """
    Display detailed information about a specific order
    """
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user
    )
    
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)