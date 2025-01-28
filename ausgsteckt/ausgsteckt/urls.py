from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views as flatpages_views
from django.urls import include, path, reverse_lazy
from django.views import defaults as default_views
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url=reverse_lazy("buschenschank:buschenschank_map")), name="index"),
    path("buschenschank/", include("buschenschank.urls")),
    path("osm/", include("data_quality.urls")),
    path("impressum/", flatpages_views.flatpage, {"url": "/impressum/"}, name="impressum"),
    path("about/", flatpages_views.flatpage, {"url": "/about/"}, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("404/", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
        path("500/", default_views.server_error),
    ]
