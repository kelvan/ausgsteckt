from django.views.generic import ListView
from django.db.models import Q

from buschenschank.models import Buschenschank


class IncompleteBuschenschankList(ListView):
    model = Buschenschank
    template_name = 'data_quality/buschenschank_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        addr_exclude = Q(
            tags__has_keys=[
                'addr:housenumber', 'addr:city', 'addr:country', 'addr:postcode'
            ],
            tags__has_any_keys=['addr:street', 'addr:place']
        )
        contact_exclude = Q(
            tags__has_keys=['contact:phone', 'contact:email'],
            tags__has_any_keys=['website', 'contact:website']
        )
        return queryset.exclude(addr_exclude and contact_exclude)
