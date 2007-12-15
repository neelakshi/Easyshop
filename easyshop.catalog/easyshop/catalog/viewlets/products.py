# zope imports
from zope.component import queryUtility

# Zope imports
from ZTUtils import make_query       

# plone imports
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize.instance import memoize

# Five imports
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# CMFPlone imports
from Products.CMFPlone import Batch      

# Easyshop imports
from easyshop.core.interfaces import INumberConverter
from easyshop.core.interfaces import IPhotoManagement
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IPropertyManagement
from easyshop.core.interfaces import IPrices
from easyshop.core.interfaces import ICurrencyManagement
from easyshop.core.interfaces import IFormats

class ProductsViewlet(ViewletBase):
    """
    """
    render = ViewPageTemplateFile('products.pt')

    @memoize
    def getFormatInfo(self):
        """
        """
        # Could be overwritten to provide fixed category views.
        # s. DemmelhuberShop
        return IFormats(self.context).getFormats()

    def getImages(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            path = {"query" : "/".join(self.context.getPhysicalPath()),
                    "depth" : 1},
            portal_type = "ESImage",
            sort_on = "getObjPositionInParent",
        )
        
        return brains
        
    def getInfo(self):
        """
        """
        batch = self._getBatch()
        # This optimized for speed, as we need _getBatch here anyway.
        # So there is no need of an extra method call within the page 
        # template to get informations we have here already. Same is true 
        # for format infos, see below
        batch_infos = {
            "previous_url"     : self._getPreviousUrl(batch),
            "previous"         : batch.previous,
            "next_url"         : self._getNextUrl(batch),
            "next"             : batch.next,
            "last_url"         : self._getLastUrl(batch),
            "navigation_list"  : batch.navlist,
            "number_of_pages"  : batch.numpages,
            "page_number"      : batch.pagenumber,
        }
        
        sorting = self.request.get("sorting", None)

        f = self.getFormatInfo()
        products_per_line = f["products_per_line"]
        
        line   = []
        products = []        
        for index, product in enumerate(batch):

            # Price
            cm = ICurrencyManagement(self.context)
            price = IPrices(product).getPriceForCustomer()
            price = cm.priceToString(price, symbol="symbol", position="before")
                                    
            # Photo
            image = IPhotoManagement(product).getMainPhoto()
            if image is not None:
                image = "%s/image_%s" % (image.absolute_url(), f.get("image_size"))
                
            t = f.get("text")
            if t == "description":
                text = product.getDescription()
            elif t == "short_text":
                text = product.getShortText()
            elif t == "text":
                text = product.getText()
            else:
                text = ""

            # CSS Class
            if (index + 1) % products_per_line == 0:
                klass = "last"
            else:
                klass = "notlast"
                            
            line.append({
                "title"                    : product.Title(),
                "short_title"              : product.getShortTitle() or product.Title(),
                "text"                     : text,
                "url"                      : "%s?sorting=%s" % (product.absolute_url(), sorting),
                "image"                    : image,
                "price"                    : price,
                "class"                    : klass,
            })
            
            if (index + 1) % products_per_line == 0:
                products.append(line)
                line = []
        
        # the rest        
        products.append(line)            
        
        # Return format infos here, because we need it anyway in this method
        # This is for speed reasons. See above.
        return {
            "products"    : products, 
            "batch_info"  : batch_infos,
            "format_info" : f,
        }

    def getProperties(self):
        """
        """
        u = queryUtility(INumberConverter)
        cm = ICurrencyManagement(self.context)
                
        selected_properties = {}
        for name, value in self.request.form.items():
            if name.startswith("property"):
                selected_properties[name[9:]] = value

        pm = IPropertyManagement(self.context)
        
        result = []
        for property in pm.getProperties():
            options = []
            for option in property.getOptions():

                # generate value string
                name  = option["name"]
                price = option["price"]

                if price != "":
                    price = u.stringToFloat(price)
                    price = cm.priceToString(price, "long", "after")
                    content = "%s %s" % (name, price)
                else:
                    content = name
                        
                # is option selected?
                selected = name == selected_properties.get(property.getId(), False)
                
                options.append({
                    "content"  : content,
                    "value"    : name,
                    "selected" : selected,
                })            
                
            result.append({
                "id"      : property.getId(),
                "title"   : property.Title(),
                "options" : options,
            })

        return result

    @memoize
    def getTdWidth(self):
        """
        """
        return "%s%%" % (100 / self.getFormatInfo().get("products_per_line"))

    def _getBatch(self):
        """
        """
        # Calculate products per page
        fi = self.getFormatInfo()
        products_per_page = fi.get("lines_per_page") * \
                            fi.get("products_per_line")        

        # Get all products                    
        mtool = getToolByName(self.context, "portal_membership")        
        sorting = self.request.get("sorting", None)
        try:
            sorted_on, sort_order = sorting.split("-")
        except (AttributeError, ValueError):
            sorted_on  = "price"
            sort_order = "desc"
        
        pm = IProductManagement(self.context)
        products = pm.getAllProducts(sorted_on=sorted_on,
                                     sort_order = sort_order)

        # Get start page                             
        b_start  = self.request.get('b_start', 0);

        # Calculate Batch
        return Batch(products, products_per_page, int(b_start), orphan=0);

    def _getLastUrl(self, batch):
        """
        """
        query = make_query(self.request.form, {batch.b_start_str:(batch.numpages-1) * batch.length})
        return "%s?%s" % (self.context.absolute_url(), query)

    def _getNextUrl(self, batch):
        """
        """
        try:
            start_str = batch.next.first
        except AttributeError:
            start_str = None 
            
        query = make_query(self.request.form, {batch.b_start_str:start_str})
        return "%s?%s" % (self.context.absolute_url(), query)

    def _getPreviousUrl(self, batch):
        """
        """
        try:
            start_str = batch.previous.first
        except AttributeError:
            start_str = None 
            
        query = make_query(self.request.form, {batch.b_start_str:start_str})
        return "%s?%s" % (self.context.absolute_url(), query)