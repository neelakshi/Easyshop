# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports 
from base import EasyShopTestCase
from easyshop.shop.tests import utils
from easyshop.core.interfaces import ICompleteness
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IPaymentProcessing
from easyshop.core.interfaces import IType

class TestDirectDebit(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestDirectDebit, self).afterSetUp()
        
        self.login("newmember")
        cm = ICustomerManagement(self.shop)
        self.customer = cm.getAuthenticatedCustomer()
        
        self.customer.invokeFactory(
            "DirectDebit",
            id = "directdebit",
            )
        
    def testGetType(self):
        """
        """
        dd = self.customer["directdebit"]
        self.assertEqual(IType(dd).getType(), "direct-debit")

    def testIsComplete(self):
        """
        """
        dd = self.customer["directdebit"]                
        self.assertEqual(ICompleteness(dd).isComplete(), False)
                    
        dd.setAccountNumber("47114711")
        self.assertEqual(ICompleteness(dd).isComplete(), False)
                
        dd.setBankIdentificationCode("50010000")
        self.assertEqual(ICompleteness(dd).isComplete(), False)
        
        dd.setName("John Doe")
        self.assertEqual(ICompleteness(dd).isComplete(), False)
                
        dd.setBankName("Deutsche Bank")
        self.assertEqual(ICompleteness(dd).isComplete(), True)        
        
    def testProcess(self):
        """
        """
        dd = self.customer["directdebit"]                
        self.assertEqual(IPaymentProcessing(dd).process(), "NOT_PAYED")
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDirectDebit))
    return suite
                                               