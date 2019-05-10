from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib import admin
from django.views.generic import RedirectView
from django.views import defaults as default_views
from django.contrib.flatpages import views as flatpages_views


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
    url(
        r'^impressum/$', flatpages_views.flatpage,
        {'url': '/impressum/'}, name='impressum'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(
            r'^404/$', default_views.page_not_found,
            kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
