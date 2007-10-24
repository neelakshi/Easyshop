# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IValidity
from easyshop.core.interfaces import IPriceCriteria
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import IShopManagement

class PriceCriteriaValidity:
    """Adapter which provides IValidity for price criteria content
    objects.
    """    
    implements(IValidity)
    adapts(IPriceCriteria)

    def __init__(self, context):
        self.context = context
        
    def isValid(self, product=None):
        """Checks whether the total price of the cart is greater than the
        entered price.
        """
        shop = IShopManagement(self.context).getShop()
        cart = ICartManagement(shop).getCart()
        
        if cart is None:
            cart_price = 0.0
        else:           
            cart_price = IPrices(cart).getPriceForCustomer(with_shipping=False)

        if cart_price > self.context.getPrice():
            return True
        return False