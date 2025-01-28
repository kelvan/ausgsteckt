from django.urls import re_path
from django.views.generic.base import TemplateView

from .apps import DataQualityConfig
from .views import BrokenURLView, IncompleteBuschenschankList

app_name = DataQualityConfig.name

urlpatterns = [
    re_path(r"^$", TemplateView.as_view(template_name="data_quality/overview.html"), name="overview"),
    re_path(
        r"^fixme/buschenschank/(?P<cityname>[^\/\\<>;,]+)?/?$",
        IncompleteBuschenschankList.as_view(),
        name="fixme_buschenschank",
    ),
    re_path(r"^fixme/websites/?$", BrokenURLView.as_view(), name="fixme_websites"),
]
