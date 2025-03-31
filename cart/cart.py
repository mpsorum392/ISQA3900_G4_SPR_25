from decimal import Decimal
from copy import deepcopy
from django.conf import settings
from products.models import Product


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        # If no cart exists or it isn't a dict, reset it.
        if not cart or not isinstance(cart, dict):
            cart = {}
        else:
            # Convert any non-dict item (e.g., integer quantity) into a dict.
            for key, value in cart.items():
                if not isinstance(value, dict):
                    try:
                        product = Product.objects.get(id=key)
                        # Assume the old value is the quantity.
                        cart[key] = {'quantity': value, 'price': str(product.price)}
                    except Product.DoesNotExist:
                        # Fallback: set price to '0' if the product is missing.
                        cart[key] = {'quantity': value, 'price': '0'}
        # Save the cleaned cart back into the session.
        self.session[settings.CART_SESSION_ID] = cart
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        Work on a deep copy so that modifications don't affect session data.
        """
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart copy.
        products = Product.objects.filter(id__in=product_ids)
        cart = deepcopy(self.cart)
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            # Convert price to Decimal for calculations.
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] if isinstance(item, dict) else item for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it is saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Calculate the total cost of the items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values() if isinstance(item, dict))

    def clear(self):
        """
        Remove the cart from the session.
        """
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]
            self.save()
