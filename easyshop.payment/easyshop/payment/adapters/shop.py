# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.catalog.content.product import Product
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentMethodManagement
from easyshop.core.interfaces import IPaymentPrices
from easyshop.core.interfaces import IPaymentPrice
from easyshop.core.interfaces import ISelectablePaymentMethod
from easyshop.core.interfaces import IShop
from easyshop.core.interfaces import ITaxes
from easyshop.core.interfaces import IValidity

class PaymentMethodManagement:
    """An adapter which provides IPaymentMethodManagement for shop content objects.
    """
    implements(IPaymentMethodManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context
        self.paymentmethods = self.context.paymentmethods

    def deletePaymentMethod(self, id):
        """
        """
        try:
            self.context.paymentmethods.manage_delObjects(id)
        except AttributeError:
            return False

        return True

    def getPaymentMethod(self, id):
        """Returns payment method by given id.
        """
        try:
            return self.paymentmethods[id]
        except KeyError:
            return None

    def getPaymentMethods(self, check_validity=False):
        """Returns the payment methods on shop level. 
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        result = []
        for object in self.paymentmethods.objectValues():

            if check_validity and \
               IValidity(object).isValid(object) == False:
                continue                    
            
            if mtool.checkPermission("View", object) is not None:
                result.append(object)
        
        return result
            
    def getSelectablePaymentMethods(self, check_validity=False):
        """Returns payment method which are selectable by a customer.
        """
        mtool = getToolByName(self.context, "portal_membership")
            
        result = []
        for object in self.paymentmethods.objectValues():

            if ISelectablePaymentMethod.providedBy(object) == False:
                continue

            if check_validity and\
               IValidity(object).isValid(object) == False:
                continue                    
            
            if mtool.checkPermission("View", object) is not None:
                result.append(object)
        
        return result
            
class PaymentPrices:
    """
    """
    implements(IPaymentPrices)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def getPaymentPrices(self):
        """
        """
        prices = self.context.paymentprices.objectValues("PaymentPrice")
        
        result = []
        for price in prices:
            if IPaymentPrice.providedBy(price) == False:
                continue
                
            result.append(price)    
        
        return result
        
    def getPriceGross(self):
        """Returns the first valid price.
        """
        for price in self.getPaymentPrices():
            if IValidity(price).isValid() == True:
                return price.getPrice()

        return 0

    # Todo: Optimize. The next methods are the same as for shipping tax
    # calculations
    
    def getPriceForCustomer(self):
        """
        """
        return self.getPriceNet() + self.getTaxForCustomer()
        
    def getPriceNet(self):
        """
        """
        return self.getPriceGross() - self.getTax()

    def getTax(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)        
        tax = taxes.getTax()
        return tax

    def getTaxForCustomer(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)        
        tax = taxes.getTaxForCustomer()

        return tax

    def getTaxRate(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)
        tax = taxes.getTaxRate()
        
        return tax

    def getTaxRateForCustomer(self):
        """
        """
        temp_payment_product = self.createTemporaryPaymentProduct()
        taxes = ITaxes(temp_payment_product)
        tax = taxes.getTaxRate()

        return tax

    def createTemporaryPaymentProduct(self):
        """
        """
        temp_payment_product = Product("payment")
        temp_payment_product.setPrice(self.getPriceGross())
        temp_payment_product.context = self.context
        
        return temp_payment_product
