
from django.template import loader, Context, RequestContext, Template

from django.template.response import SimpleTemplateResponse


class CustomTemplateResponse(SimpleTemplateResponse):
    rendering_attrs = SimpleTemplateResponse.rendering_attrs + ['_request', '_current_app']

    def __init__(self, request, template, context=None, content_type=None,
            status=None, current_app=None):

        self.template_object = template
        self._request = request
        self._current_app = current_app
        super(CustomTemplateResponse, self).__init__(
            template, context, content_type, status)

    @property
    def rendered_content(self):
        context = self.resolve_context(self.context_data)
        return self.template_object.render(context)

    def resolve_context(self, context):
        if isinstance(context, Context):
            return context
        return RequestContext(self._request, context, current_app=self._current_app)