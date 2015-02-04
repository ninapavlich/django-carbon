from django.contrib import admin

from carbon.compounds.page.admin import PageAdmin as BasePageAdmin
from carbon.compounds.page.admin import PageTagAdmin as BasePageTagAdmin
from carbon.compounds.page.admin import MenuItemInline as BaseMenuItemInline
from carbon.compounds.page.admin import MenuItemAdmin as BaseMenuItemAdmin

from .models import *

class PageAdmin(BasePageAdmin):
    pass



class PageTagAdmin(BasePageTagAdmin):
    pass


class MenuItemInline(BaseMenuItemInline):
    model = MenuItem
    


class MenuItemAdmin(BaseMenuItemAdmin):
    
    pass



admin.site.register(Page, PageAdmin)
admin.site.register(PageTag, PageTagAdmin)
admin.site.register(MenuItem, MenuItemAdmin)