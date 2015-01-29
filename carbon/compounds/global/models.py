from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


from carbon.atoms.models.content import TemplateMolecule




class Template(TemplateMolecule):

    @staticmethod
    def autocomplete_search_fields():
        return ("admin_note__icontains","title__icontains")