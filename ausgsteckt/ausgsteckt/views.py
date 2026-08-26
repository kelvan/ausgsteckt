from django.contrib.flatpages.views import flatpage
from django.http import Http404, JsonResponse
from django.utils.translation import get_language, get_supported_language_variant
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin


def localized_flatpage(request, base_url):
    """Resolves base_url="about" to FlatPage.url "/de/about/" or "/en/about/",
    falling back to German if the current language has no translation yet."""
    language = get_supported_language_variant(get_language())
    try:
        return flatpage(request, f"/{language}/{base_url}/")
    except Http404:
        if language == "de":
            raise
        return flatpage(request, f"/de/{base_url}/")


class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

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
    def render_to_response(self, context, **response_kwargs):
        # Look for a 'format=json' GET argument
        if "application/json" in self.request.META.get("HTTP_ACCEPT", ""):
            return self.render_to_json_response(context)
        else:
            return super().render_to_response(context, **response_kwargs)


class PageTitleMixin:
    page_title = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # ty: ignore[unresolved-attribute]
        context["page_title"] = self.get_page_title()
        return context
