import os
import csv

from django.conf import settings
from django.http import Http404
from django.views.generic import ListView, TemplateView
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
        contact_exclude = (
            Q(
                tags__has_any_keys=['website', 'contact:website']
            ) and Q(
                tags__has_any_keys=['contact:phone', 'phone']
            ) and Q(
                tags__has_any_keys=['contact:email', 'email'],
            )
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
        context['city'] = self.kwargs.get('cityname')
        return context


class BrokenURLView(TemplateView):
    template_name = 'data_quality/broken_urls.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        report_path = os.path.join(
            settings.MEDIA_ROOT, 'broken_websites_report.csv'
        )

        if not os.path.exists(report_path):
            raise Http404()

        with open(report_path) as csvfile:
            context['error_list'] = list(csv.DictReader(csvfile))

        return context
