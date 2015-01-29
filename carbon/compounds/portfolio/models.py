from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from carbon.atoms.models.content import ContentMolecule, CategoryMolecule, OrderedItemMolecule
from carbon.atoms.models.media import MediaMolecule

class Project(ContentMolecule):
    
    def get_absolute_url(self):
    	return reverse('projects_project', kwargs = {'path': self.get_url_path() })   


class ProjectCategoryItem(OrderedItemMolecule):
    category = models.ForeignKey('portfolio.ProjectCategory')
    item = models.ForeignKey('portfolio.Project')

    class Meta:
        unique_together = (("category", "item"),)


class ProjectCategory(CategoryMolecule):
    item_class = ProjectCategoryItem

    class Meta:
        verbose_name_plural = 'Project Categories'

    def get_absolute_url(self):
        return reverse('projects_category', kwargs = {'path': self.get_url_path() })   




class ProjectMedia(MediaMolecule):
    project = models.ForeignKey('portfolio.Project')