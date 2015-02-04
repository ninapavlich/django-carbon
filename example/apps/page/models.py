from django.db import models
from django.conf import settings


from carbon.compounds.page.models import Page as BasePage
from carbon.compounds.page.models import PageTag as BasePageTag
from carbon.compounds.page.models import MenuItem as BaseMenuItem


class Page(BasePage):

    pass


class PageTag(BasePageTag):  

    pass
        

class MenuItem(BaseMenuItem):

    pass
    
