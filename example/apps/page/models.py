from django.db import models
from django.conf import settings


from carbon.compounds.page.models import Page as BasePage
from carbon.compounds.page.models import PageTag as BasePageTag
from carbon.compounds.page.models import MenuItem as BaseMenuItem


class Page(BasePage):
	
	tags = models.ManyToManyField('page.PageTag', null=True, blank=True)

	def get_absolute_url(self):
        return reverse('pages_page', kwargs = {'path': self.get_url_path() })  

class PageTag(BasePageTag):  

	def get_absolute_url(self):
        return reverse('pages_tag', kwargs = {'path': self.get_url_path() })   
    
        

class MenuItem(BaseMenuItem):

    pass
    
