from django.views.generic import ListView
from django.db.models import Q
from django.db.models.expressions import RawSQL

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
        queryset = queryset.exclude(addr_exclude and contact_exclude)
        city = self.kwargs.get('cityname')
        if city:
            queryset = queryset.filter(tags__contains={'addr:city': city})
        # XXX no json order support in django yet
        return queryset.order_by(
            RawSQL('tags->>%s', ('addr:city',)),
            RawSQL('tags->>%s', ('addr:postcode',)),
            RawSQL('tags->>%s', ('name',))
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['overall_buschenschank_count'] = Buschenschank.objects.count()
        return context
