from carbon.compounds.portfolio.views import ProjectDetailView as BaseProjectDetailView
from carbon.compounds.portfolio.views import ProjectCategoryView as BaseProjectCategoryView

from .models import *

class ProjectDetailView(BaseProjectDetailView):

    model = Project


class ProjectCategoryView(BaseProjectCategoryView):

    model = ProjectCategory