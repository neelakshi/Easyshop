# zope imports
from zope.interface import Interface
from zope.interface import Attribute

class IOrder(Interface):
    """An order of products.
    """
    
class IOrderManagement(Interface):
    """Provides methods to manage order content objects.
    """
    def addOrder(customer=None, cart=None):
        """Adds a new order.        
        """

    def copyCustomerToOrder(customer, order):
        """copys customer to order.
        """

    def getOrders(filter=None):
        """Returns orders filtered by given filter.
        """

    def getOrdersForAuthenticatedCustomer():
        """Returns all orders for the actual customer
        """

    def createOrderId():
        """Creates a new unique order id
        """

    def getOrderByUID(uid):
        """Returns order by given uid.        
        """
        
class IOrdersContainer(Interface):
    """A container to hold orders.
    """
    
class IOrderSubmitted(Interface):
    """An event fired when an order has been submitted.
    """    
    context = Attribute("The order that has been submitted")
    
class IOrderPayed(Interface):
    """An event fired when an order has been payed.
    """    
    context = Attribute("The order that has been payed")
    
class IOrderSent(Interface):
    """An event fired when an order has been sent
    """    
    context = Attribute("The order that has been sent")
    
class IOrderClosed(Interface):
    """An event fired when an order has been closed
    """    
    context = Attribute("The order that has been closed")