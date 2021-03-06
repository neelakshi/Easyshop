# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IFormatterInfos
from Products.EasyShop.interfaces import IPhotoManagement

class TestFormatterInfos(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        super(TestFormatterInfos, self).afterSetUp()
        self.fi_1 = IFormatterInfos(self.shop)
        self.fi_2 = IFormatterInfos(self.shop.categories.category_1)
        
    def testGetText(self):
        """
        """
        self.assertEqual(self.fi_1.getText(), "short_text") 

    def testGetFormatter(self):
        """
        """        
        self.assertEqual(self.fi_1.getFormatter().getId(), "formatter")
        self.assertEqual(self.fi_2.getFormatter().getId(), "formatter")
                
    def testGetFormatInfosAsDict(self):
        """
        """
        fi_1 = self.fi_1.getFormatInfosAsDict()
        fi_2 = self.fi_2.getFormatInfosAsDict()
            
        self.assertEqual(fi_1["lines_per_page"], 1)
        self.assertEqual(fi_1["products_per_line"], 2)
        self.assertEqual(fi_1["image_size"], "mini")
        self.assertEqual(fi_1["text"], "short_text")
        self.assertEqual(fi_1["product_height"], 0)

        self.assertEqual(fi_2["lines_per_page"], 1)
        self.assertEqual(fi_2["products_per_line"], 2)
        self.assertEqual(fi_2["image_size"], "mini")
        self.assertEqual(fi_2["text"], "short_text")
        self.assertEqual(fi_2["product_height"], 0)
                
    def testGetLinesPerPage(self):
        """
        """
        self.assertEqual(self.fi_1.getLinesPerPage(), 1)
        self.assertEqual(self.fi_2.getLinesPerPage(), 1)
        
    def testGetProductsPerLine(self):
        """
        """
        self.assertEqual(self.fi_1.getProductsPerLine(), 2)
        self.assertEqual(self.fi_2.getProductsPerLine(), 2)
        
    def testGetImageSize(self):
        """
        """
        self.assertEqual(self.fi_1.getImageSize(), "mini")
        self.assertEqual(self.fi_2.getImageSize(), "mini")
        
    def testHasFormatter(self):
        """
        """    
        self.assertEqual(self.fi_1.hasFormatter(), True)
        self.assertEqual(self.fi_2.hasFormatter(), False)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestFormatterInfos))
    return suite
                                               