from django.conf.urls import url
from django.views.generic.base import TemplateView

from .apps import DataQualityConfig
from .views import IncompleteBuschenschankList, BrokenURLView

app_name = DataQualityConfig.name

urlpatterns = [
    url(
        r'^$',
        TemplateView.as_view(template_name='data_quality/overview.html'),
        name='overview'
    ),
    url(
        r'fixme/buschenschank/(?P<cityname>[^\d\/\\<>;,]+)?/?$',
        IncompleteBuschenschankList.as_view(),
        name='fixme_buschenschank'
    ),
    url(
        r'fixme/websites/?$', BrokenURLView.as_view(), name='fixme_websites'
    )
]
