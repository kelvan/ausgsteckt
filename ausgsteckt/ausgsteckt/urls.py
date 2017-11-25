from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(
        r'^$', RedirectView.as_view(
            url=reverse_lazy('buschenschank:buschenschank_map')
        ),
        name='index'
    ),
    url(r'^buschenschank/', include('buschenschank.urls')),
    url(r'^osm/', include('data_quality.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
