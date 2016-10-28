from django.shortcuts import render

from ausgsteckt.views import HybridDetailView
from .models import Buschenschank


class BuschenschankDetails(HybridDetailView):
    model = Buschenschank
    
    def get_data(self, context):
        buschenschank = context['buschenschank']
        return {
            'name': buschenschank.name,
            'osm_id': buschenschank.osm_id,
            'tags': buschenschank.tags
        }
