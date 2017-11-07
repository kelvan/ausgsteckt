from django.conf.urls import url, include
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .apps import BuschenschankConfig
from .models import Buschenschank, Region
from .views import (
    BuschenschankDetails, PublicBuschenschankGeoJsonView, RegionListView,
    RegionDetailView
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
            PublicBuschenschankGeoJsonView.as_view()
        ),
        name='buschenschank.geojson'
    ),
    url(
        r'region/(?P<pk>\d+)', RegionDetailView.as_view(),
        name='region_details'
    ),
    url(
        r'regions/', RegionListView.as_view(),
        name='region_list'
    )
]
