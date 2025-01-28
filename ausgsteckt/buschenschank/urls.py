from django.urls import re_path
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from .apps import BuschenschankConfig
from .views import (
    BuschenschankAPIDetailView,
    BuschenschankDetailView,
    MainMapView,
    OpenTodayListView,
    PublicBuschenschankGeoJsonView,
    RegionDetailView,
    RegionListView,
    SearchView,
)

app_name = BuschenschankConfig.name

urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="data_quality/overview.html"), name="overview"),
    re_path(r"^map/$", MainMapView.as_view(), name="buschenschank_map"),
    re_path(
        r"^api/buschenschank/(?P<pk>\d+)/$", BuschenschankAPIDetailView.as_view(), name="buschenschank_details_api"
    ),
    re_path(r"^buschenschank/(?P<pk>\d+)/$", BuschenschankDetailView.as_view(), name="buschenschank_details"),
    re_path(
        r"^buschenschank/(?P<pk>\d+)-(?P<slug>[\w_-]+)/$",
        BuschenschankDetailView.as_view(),
        name="buschenschank_details",
    ),
    re_path(
        r"^data.geojson$", cache_page(60 * 15)(PublicBuschenschankGeoJsonView.as_view()), name="buschenschank.geojson"
    ),
    re_path(r"region/(?P<pk>\d+)/", RegionDetailView.as_view(), name="region_details"),
    re_path(r"region/(?P<pk>\d+)-(?P<slug>[\w_-]+)/", RegionDetailView.as_view(), name="region_details"),
    re_path(r"regions/", RegionListView.as_view(), name="region_list"),
    re_path(r"open/", OpenTodayListView.as_view(), name="open_list"),
    re_path(r"search/", SearchView.as_view(), name="search"),
]
