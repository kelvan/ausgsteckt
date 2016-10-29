import logging
from itertools import chain

import overpy

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
        buschenschank = Buschenschank.objects.filter(osm_id=element.id).first()
        if buschenschank is None:
            buschenschank = Buschenschank(osm_id=element.id)

        name = element.tags.get('name')
        if name is None:
            return False
        buschenschank.name = name
        buschenschank.coordinates = Point(float(element.lon), float(element.lat))
        buschenschank.tags = element.tags
        buschenschank.save()

    def handle(self, *args, **options):
        api = overpy.Overpass()
        buschenschank = api.query(
            '(node["cuisine"~"buschenschank"];way["cuisine"~"buschenschank"];relation["cuisine"~"buschenschank"]);out center meta;'
        ).nodes
        heuriger = api.query(
            '(node["cuisine"~"heuriger"];way["cuisine"~"heuriger"];relation["cuisine"~"heuriger"]);out center meta;'
        ).nodes
        for element in chain(buschenschank, heuriger):
            self.save_buschenschank(element)
