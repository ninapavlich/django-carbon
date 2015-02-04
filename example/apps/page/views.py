from carbon.compounds.page.views import PageDetail as BasePageDetail
from carbon.compounds.page.views import PageTagView as BasePageTagView

from .models import *


class PageDetail(BasePageDetail):

    model = Page

    



class PageTagView(BasePageTagView):

    model = PageTag