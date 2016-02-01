"""
This file was generated with the customdashboard management command and
contains the class for the main dashboard.

To activate your index dashboard add the following to your settings.py::
    GRAPPELLI_INDEX_DASHBOARD = 'project.dashboard.CustomIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.modules import DashboardModule
from grappelli.dashboard.utils import get_admin_site_name




# class AdminTasksDashboardModule(DashboardModule):

#     title = 'Admin Tasks'
#     template = 'admin/admin_tasks.html'
    
#     def getActionMessage(self, item_count):
#         if item_count == 0:
#             return ""
#         else:
#             return "There are new admin tasks."

    
#     def getVerbPhrase(self, count):
#         if count >= 1:
#             return str(count)
#         else:
#             return "No"

#     def init_with_context(self, context):
#         if self._initialized:
#             return
#         new_children = []
        
#         unconnected_urls = LegacyURL.objects.needs_redirect()
#         if len(unconnected_urls) > 0:
#             new_children.append({
#                 'title': "There are %s urls to be redirected"%(self.getVerbPhrase(len(unconnected_urls))), 
#                 'url': "/admin/site_admin/legacyurl/?_redirect_path=0",
#                 "external":False,
#             })

#         total_count = len(unconnected_urls)

#         self.admin_message = self.getActionMessage(total_count)
#         self.children = new_children
#         self._initialized = True


class BaseAdminDashboard(Dashboard):
    
    #sidebar_model
    #main_model
    

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        main_link_sets = self.main_model.objects.all()
        for link_set in main_link_sets:

            children = link_set.get_children()
            child_links = [link.model_path for link in children]
            # -- Django Admin

            classes = ['grp-closed'] if not link_set.open_by_default else []
            self.children.append(modules.AppList(
                title=_(link_set.title),
                column=1,
                collapsible=True,
                models=child_links,
                css_classes=classes
            ))
        
        
        classes = ['grp-closed'] if main_link_sets.count()>0 else []

        # -- Django Admin
        self.children.append(modules.AppList(
            title=_('All Models'),
            column=1,
            collapsible=True,
            css_classes=classes
        ))

         

        sidebar_link_sets = self.sidebar_model.objects.all()
        for link_set in sidebar_link_sets:

            children = []
            child_links = link_set.get_children()
            for child_link in child_links:
                children.append({
                    'title':child_link.title,
                    'url':child_link.url,
                    'external':False
                })

            # append another link list module for "support".
            self.children.append(modules.LinkList(
                link_set.title,
                column=2,
                children=children
            ))
        

        
        # self.children.append(AdminTasksDashboardModule(

        #     _('Admin Tasks'),
        #     column=2,

        # ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=5,
            collapsible=False,
            column=2,
        ))


