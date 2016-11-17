from django.conf.urls import url

from .views import IncompleteBuschenschankList


urlpatterns = [
    url(r'fixme/incomplete_buschenschank/$', IncompleteBuschenschankList.as_view()),
]
