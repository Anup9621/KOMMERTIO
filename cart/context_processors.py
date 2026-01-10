"""
Cart Context Processor
Makes cart available in all templates
"""

from .cart import Cart


def cart(request):
    """
    Return cart instance to be used in templates
    """
    return {'cart': Cart(request)}