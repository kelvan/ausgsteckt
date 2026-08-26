from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path, reverse_lazy
from django.views import defaults as default_views
from django.views.generic import RedirectView

from .views import localized_flatpage

urlpatterns: list[URLPattern | URLResolver] = [
    path("admin/", admin.site.urls),
]

# The language-switch endpoint (set_language) must itself be reachable through
# a language-prefixed URL. LocaleMiddleware force-overrides the active
# language to the site default on any *unprefixed* path (since
# prefix_default_language=False treats "no prefix" as "default language"),
# which broke set_language's own URL-translation lookup when switching away
# from the default language. Keeping it inside i18n_patterns() means the
# navbar's {% url 'set_language' %} always posts to the current language's
# own prefix, so that override never kicks in for it.
urlpatterns += i18n_patterns(
    path("i18n/", include("django.conf.urls.i18n")),
    path("", RedirectView.as_view(url=reverse_lazy("buschenschank:buschenschank_map")), name="index"),
    path("buschenschank/", include("buschenschank.urls")),
    path("osm/", include("data_quality.urls")),
    path("impressum/", localized_flatpage, {"base_url": "impressum"}, name="impressum"),
    path("about/", localized_flatpage, {"base_url": "about"}, name="about"),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("404/", default_views.page_not_found, kwargs={"exception": Exception("Page not Found")}),
        path("500/", default_views.server_error),
    ]
