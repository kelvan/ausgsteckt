from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .apps import BuschenschankConfig
from .views import (
    MainMapView, BuschenschankDetailView, BuschenschankAPIDetailView,
    PublicBuschenschankGeoJsonView, RegionListView,
    RegionDetailView, SearchView, OpenTodayListView
)

app_name = BuschenschankConfig.name

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='data_quality/overview.html'),
        name='overview'),
    url(r'^map/$', MainMapView.as_view(), name='buschenschank_map'),
    url(
        r'^api/buschenschank/(?P<pk>\d+)/$',
        BuschenschankAPIDetailView.as_view(),
        name='buschenschank_details_api'
    ),
    url(
        r'^buschenschank/(?P<pk>\d+)/$', BuschenschankDetailView.as_view(),
        name='buschenschank_details'
    ),
    url(
        r'^buschenschank/(?P<pk>\d+)-(?P<slug>[\w_-]+)/$',
        BuschenschankDetailView.as_view(),
        name='buschenschank_details'
    ),
    url(
        r'^data.geojson$',
        cache_page(60 * 15)(PublicBuschenschankGeoJsonView.as_view()),
        name='buschenschank.geojson'
    ),
    url(
        r'region/(?P<pk>\d+)/',
        RegionDetailView.as_view(),
        name='region_details'),
    url(
        r'region/(?P<pk>\d+)-(?P<slug>[\w_-]+)/',
        RegionDetailView.as_view(), name='region_details'),
    url(r'regions/', RegionListView.as_view(), name='region_list'),
    url(r'open/', OpenTodayListView.as_view(), name='open_list'),
    url(r'search/', SearchView.as_view(), name='search')
]
