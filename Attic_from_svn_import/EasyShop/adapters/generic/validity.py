# zope imports
from zope.interface import implements
from zope.component import adapts
  
# EasyShop imports
from Products.EasyShop.interfaces import ICustomerPaymentMethod
from Products.EasyShop.interfaces import IPaymentManagement
from Products.EasyShop.interfaces import IValidity
from Products.EasyShop.interfaces import IShopManagement
from Products.EasyShop.interfaces import IType

class ValidityManagement(object):
    """An adapter which provides IValidity for several classes. See 
    configure.zcml for more information
    """
    implements(IValidity)
     
    def __init__(self, context):
        """
        """
        self.context = context

    def isValid(self, product=None):
        """Returns true if all contained criteria are true.
        """
        # To be true all criteria must be true (AND)
        for criteria in self.context.objectValues():
            # First try "isValid" on the criterion. This maybe makes it easier
            # to write own 3rd party criteria without the need to write an 
            # adapter.
            try:
                if criteria.isValid(product) == False:
                    return False
            except AttributeError:
                # Then take the adapter. This makes it OTOH easier to overwrite the 
                # default behaviour of the default criterias
                if IValidity(criteria).isValid(product) == False:
                    return False
                                            
        return True
        
        
class CustomerPaymentValidityManagement(ValidityManagement):
    """An adapter which provides IValidity for customer payment methods.
    """
    implements(IValidity)
    adapts(ICustomerPaymentMethod)

    def __init__(self, context):
        """
        """
        super(CustomerPaymentValidityManagement, self).__init__(context)
    
    def isValid(self, product=None):
        """Returns true if the corresponding payment validator is not False and
        all contained criteria are True.
        """
        # First we check the general validity. For that we try to get the
        # corresponding payment validator.
        type   = IType(self.context).getType()
        pm     = IPaymentManagement(IShopManagement(self.context).getShop())
        method = pm.getPaymentMethod(type)
        
        # Only if we find one, we check validity. If we didn't find one, we
        # consider the general validity as fulfilled.
        if method and IValidity(method).isValid() == False:
            return False
        
        # If the non-validity isn't proved we check the criteria of context
        # (a customer payment method)
        return super(CustomerPaymentValidityManagement, self).isValid(product)