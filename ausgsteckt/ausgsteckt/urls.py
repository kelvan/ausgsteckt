from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from djgeojson.views import GeoJSONLayerView

from buschenschank.models import Buschenschank


urlpatterns = [
    url(r'^map/$', TemplateView.as_view(template_name='buschenschank/map.html')),
    url(r'^admin/', admin.site.urls),
    url(
        r'^data.geojson$', GeoJSONLayerView.as_view(model=Buschenschank, geometry_field='coordinates'), 
        name='buschenschank.geojson'
    )
]
