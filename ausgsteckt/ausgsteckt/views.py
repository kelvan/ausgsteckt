from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):

    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if 'application/json' in self.request.META.get('HTTP_ACCEPT'):
            return self.render_to_json_response(context)
        else:
            return super().render_to_response(context)


class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        return context