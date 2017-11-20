import logging

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.core.serializers import serialize

from ausgsteckt.views import HybridDetailView
from .models import Buschenschank, Region

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


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


class BuschenschankDetailView(DetailView):
    model = Buschenschank
    template_name = 'buschenschank/buschenschank_detail.html'


class PublicBuschenschankGeoJsonView(ListView):
    model = Buschenschank

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_removed=False)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        data = serialize('geojson', self.object_list,
                         geometry_field='coordinates', fields=('pk', 'name',))
        return HttpResponse(data, content_type='application/json')


class RegionListView(ListView):
    model = Region


class RegionDetailView(DetailView):
    model = Region


class SearchView(TemplateView):
    template_name = 'buschenschank/search_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        if q:
            context['results'] = Buschenschank.objects.filter(name__icontains=self.request.GET.get('q'))
        return context