from django.db import models
from django.conf import settings

from carbon.compounds.portfolio import Project as BaseProject
from carbon.compounds.portfolio import ProjectCategoryItem as BaseProjectCategoryItem
from carbon.compounds.portfolio import ProjectCategory as BaseProjectCategory
from carbon.compounds.portfolio import ProjectMedia as BaseProjectMedia

class Project(BaseProject):
    pass

class ProjectCategoryItem(BaseProjectCategoryItem):
    pass

class ProjectCategory(BaseProjectCategory):
    pass

class ProjectMedia(BaseProjectMedia):
    pass