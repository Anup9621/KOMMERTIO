"""
Shopping Cart Class
Session-based cart management with add, remove, update, and clear functionality
"""

from decimal import Decimal
from django.conf import settings
from store.models import Product


class Cart:
    """
    Shopping cart stored in session
    """
    
    def __init__(self, request):
        """
        Initialize the cart from session
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity
        
        Args:
            product: Product instance to add
            quantity: Quantity to add (default: 1)
            update_quantity: If True, replace quantity instead of adding (default: False)
        """
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.get_price())
            }
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product):
        """
        Remove a product from the cart
        
        Args:
            product: Product instance to remove
        """
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def save(self):
        """
        Mark the session as modified to ensure it's saved
        """
        self.session.modified = True
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Calculate the total price of all items in the cart
        """
        return sum(
            Decimal(item['price']) * item['quantity'] 
            for item in self.cart.values()
        )
    
    def clear(self):
        """
        Remove all items from the cart
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def update_quantity(self, product_id, quantity):
        """
        Update the quantity of a product in the cart
        
        Args:
            product_id: ID of the product
            quantity: New quantity
        """
        product_id = str(product_id)
        
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
                self.save()
            else:
                # Remove if quantity is 0 or less
                del self.cart[product_id]
                self.save()