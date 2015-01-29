from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.content import ContentMolecule, CategoryMolecule, OrderedItemMolecule
from carbon.atoms.models.media import MediaMolecule

class Project(ContentMolecule):
    pass


class ProjectCategoryItem(OrderedItemMolecule):
    category = models.ForeignKey('portfolio.ProjectCategory')
    item = models.ForeignKey('portfolio.Project')

    class Meta:
        unique_together = (("category", "item"),)


class ProjectCategory(CategoryMolecule):
    item_class = ProjectCategoryItem

    class Meta:
        verbose_name_plural = 'Project Categories'


class ProjectMedia(MediaMolecule):
    project = models.ForeignKey('portfolio.Project')