
from django.template import loader, Context, RequestContext
from django.template import Template

from django.template.response import SimpleTemplateResponse


class CustomTemplateResponse(SimpleTemplateResponse):
    rendering_attrs = SimpleTemplateResponse.rendering_attrs + ['_request', '_current_app']

    def __init__(self, request, template, context=None, content_type=None,
            status=None, current_app=None):

        self.template_content = template.content
        self._request = request
        self._current_app = current_app
        super(CustomTemplateResponse, self).__init__(
            template, context, content_type, status)

    @property
    def rendered_content(self):
        template = Template(self.template_content)
        context = self.resolve_context(self.context_data)
        content = template.render(context)
        return content

    def resolve_context(self, context):
        if isinstance(context, Context):
            return context
        return RequestContext(self._request, context, current_app=self._current_app)