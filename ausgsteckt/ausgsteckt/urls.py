from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from djgeojson.views import GeoJSONLayerView

from buschenschank.models import Buschenschank
from buschenschank.views import BuschenschankDetails


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^map/$', TemplateView.as_view(template_name='buschenschank/map.html'), name='buschenschank_map'),
    url(r'^buschenschank/details/(?P<pk>\d+)$', BuschenschankDetails.as_view(), name='buschenschank_details'),
    url(
        r'^data.geojson$', GeoJSONLayerView.as_view(model=Buschenschank, geometry_field='coordinates'),
        name='buschenschank.geojson'
    )
]
