import logging
from typing import Any

from ausgsteckt.views import HybridDetailView, PageTitleMixin
from django.core.serializers import serialize
from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Buschenschank, Region

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class MainMapView(PageTitleMixin, TemplateView):
    template_name = "buschenschank/map.html"
    page_title = _("Map")


class BuschenschankAPIDetailView(HybridDetailView):
    queryset = Buschenschank.available_objects
    template_name = "buschenschank/api/buschenschank_detail.html"

    def get_data(self, context):
        buschenschank = context["buschenschank"]
        return {"name": str(buschenschank), "osm_id": buschenschank.osm_id, "tags": buschenschank.tags}


class BuschenschankDetailView(PageTitleMixin, DetailView):
    queryset = Buschenschank.available_objects
    template_name = "buschenschank/buschenschank_detail.html"

    def get_queryset(self) -> models.QuerySet[Any]:
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(published=True)
        return queryset

    def get_page_title(self):
        return self.object.name


class PublicBuschenschankGeoJsonView(ListView):
    queryset = Buschenschank.available_objects

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        data = serialize(
            "geojson",
            self.object_list,
            geometry_field="coordinates",
            fields=(
                "pk",
                "name",
            ),
        )
        return HttpResponse(data, content_type="application/json")


class RegionListView(PageTitleMixin, TemplateView):
    template_name = "buschenschank/region_list.html"
    page_title = _("Regions")


class RegionDetailView(PageTitleMixin, DetailView):
    model = Region

    def get_page_title(self):
        return self.object.name


class SearchView(PageTitleMixin, TemplateView):
    template_name = "buschenschank/search_result.html"
    page_title = _('Search results for "{}"')
    queryset = Buschenschank.available_objects

    def get_queryset(self) -> models.QuerySet[Any]:
        queryset = super().get_queryset()
        return queryset.filter(published=True)

    def get_page_title(self):
        page_title = super().get_page_title()
        return page_title.format(self.request.GET.get("q", ""))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")
        if q:
            name_contains = Q(name__icontains=q) | Q(tags__alt_name__icontains=q)
            operator_contains = Q(tags__operator__icontains=q)
            address_contains = (
                Q(**{"tags__addr:street__icontains": q})
                | Q(**{"tags__addr:city__icontains": q})
                | Q(**{"tags__addr:postcode__icontains": q})
            )
            alt_name_contains = Q(tags__alt_name__icontains=q)
            context["results"] = self.queryset.filter(published=True).filter(
                name_contains | alt_name_contains | address_contains | operator_contains
            )
        return context


class OpenTodayListView(PageTitleMixin, ListView):
    page_title = _("Open today")

    def get_queryset(self):
        return Buschenschank.open_today.all()
