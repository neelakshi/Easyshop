# Zope imports
from zope.interface import implements

# Archetypes imports
from Products.Archetypes.atapi import BaseBTreeFolder
from Products.Archetypes.atapi import registerType

# EasyShop imports
from easyshop.carts.config import *
from Products.EasyShop.interfaces.cart import ICartsContainer

class CartsContainer(BaseBTreeFolder, EasyShopBase):
    """A simple container to hold carts.
    """
    implements(ICartsContainer)
    
registerType(CartsContainer, PROJECTNAME)