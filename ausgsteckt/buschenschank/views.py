import logging

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.core.serializers import serialize
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


from ausgsteckt.views import HybridDetailView, PageTitleMixin
from .models import Buschenschank, Region

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MainMapView(PageTitleMixin, TemplateView):
    template_name = 'buschenschank/map.html'
    page_title = _('Map')


class BuschenschankAPIDetailView(HybridDetailView):
    model = Buschenschank
    template_name = 'buschenschank/api/buschenschank_detail.html'

    def get_data(self, context):
        buschenschank = context['buschenschank']
        return {
            'name': buschenschank.name,
            'osm_id': buschenschank.osm_id,
            'tags': buschenschank.tags
        }


class BuschenschankDetailView(PageTitleMixin, DetailView):
    model = Buschenschank
    template_name = 'buschenschank/buschenschank_detail.html'

    def get_page_title(self):
        return self.object.name


class PublicBuschenschankGeoJsonView(ListView):
    model = Buschenschank

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title']
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_removed=False)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        data = serialize('geojson', self.object_list,
                         geometry_field='coordinates', fields=('pk', 'name',))
        return HttpResponse(data, content_type='application/json')


class RegionListView(PageTitleMixin, TemplateView):
    template_name = 'buschenschank/region_list.html'
    page_title = _('Regions')


class RegionDetailView(PageTitleMixin, DetailView):
    model = Region

    def get_page_title(self):
        return self.object.name


class SearchView(PageTitleMixin, TemplateView):
    template_name = 'buschenschank/search_result.html'
    page_title = _('Search results for "{}"')

    def get_page_title(self):
        page_title = super().get_page_title()
        return page_title.format(self.request.GET.get('q', ''))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            name_contains = Q(name__icontains=q)
            operator_contains = Q(tags__operator__icontains=q)
            address_contains = (Q(**{'tags__addr:street__icontains': q}) |
                                Q(**{'tags__addr:city__icontains': q}) |
                                Q(**{'tags__addr:postcode__icontains': q}))
            alt_name_contains = Q(tags__alt_name__icontains=q)
            context['results'] = Buschenschank.objects.filter(
                name_contains | alt_name_contains | address_contains | operator_contains)
        return context
