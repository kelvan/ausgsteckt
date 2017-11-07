import logging

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse
from django.core.serializers import serialize

from djgeojson.views import GeoJSONLayerView

from ausgsteckt.views import HybridDetailView
from .models import Buschenschank, Region

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class BuschenschankDetails(HybridDetailView):
    model = Buschenschank

    def get_data(self, context):
        buschenschank = context['buschenschank']
        return {
            'name': buschenschank.name,
            'osm_id': buschenschank.osm_id,
            'tags': buschenschank.tags
        }


class PublicBuschenschankGeoJsonView(ListView):
    model = Buschenschank

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_removed=False)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        data = serialize('geojson', self.object_list,
                  geometry_field='coordinates',
                  fields=('name',)
        )
        return HttpResponse(data, content_type='application/json')


class RegionListView(ListView):
    model = Region


class RegionDetailView(DetailView):
    model = Region
