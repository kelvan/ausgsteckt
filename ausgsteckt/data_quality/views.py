from django.views.generic import ListView
from django.db.models import Q

from buschenschank.models import Buschenschank


class IncompleteBuschenschankList(ListView):
    model = Buschenschank
    template_name = 'data_quality/buschenschank_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
