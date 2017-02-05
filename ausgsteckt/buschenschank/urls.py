from django.conf.urls import url, include
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .apps import BuschenschankConfig
from .models import Buschenschank, Region
from .views import (
    BuschenschankDetails, HideRemovedGeoJSONLayerView, RegionListView
)

app_name = BuschenschankConfig.name

urlpatterns = [
    url(
        r'^$', TemplateView.as_view(template_name='data_quality/overview.html'),
        name='overview'
    ),
    url(
        r'^map/$', TemplateView.as_view(template_name='buschenschank/map.html'),
        name='buschenschank_map'
    ),
    url(
        r'^buschenschank/(?P<pk>\d+)$', BuschenschankDetails.as_view(),
        name='buschenschank_details'
    ),
    url(
        r'^data.geojson$',
        cache_page(60 * 15)(
            HideRemovedGeoJSONLayerView.as_view(
                model=Buschenschank, geometry_field='coordinates'
            )
        ),
        name='buschenschank.geojson'
    ),
    url(
        r'region/(?P<pk>\d+)', DetailView.as_view(model=Region),
        name='region_details'
    ),
    url(
        r'regions/', RegionListView.as_view(),
        name='region_list'
    )
]
