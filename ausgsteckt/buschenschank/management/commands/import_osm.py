import logging
from itertools import chain

import overpass

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ...models import Buschenschank

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Command(BaseCommand):
    help = 'Import Buschenschank/Heuriger from OSM'

    def save_buschenschank(self, element):
        buschenschank = Buschenschank.objects.filter(osm_id=element['id']).first()
        if buschenschank is None:
            buschenschank = Buschenschank(osm_id=element['id'])
            
        name = element['tags'].get('name')
        if name is None:
            return False
        buschenschank.name = name
        buschenschank.coordinates = Point(element['lon'], element['lat'])
        buschenschank.tags = element['tags']
        buschenschank.save()
        
    def handle(self, *args, **options):
        # TODO fetch areas too, replace location with center of polygon
        api = overpass.API()
        buschenschank = api.Get('node["cuisine"="buschenschank"]', responseformat='json').get('elements', [])
        heuriger = api.Get('node["cuisine"="heuriger"]', responseformat='json').get('elements', [])
        for element in chain(buschenschank, heuriger):
            self.save_buschenschank(element)
