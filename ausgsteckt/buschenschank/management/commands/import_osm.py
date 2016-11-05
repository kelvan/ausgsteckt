import logging
from xml.sax import parseString

import requests

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from .overpass_parser import NodeCenterSaxParser
from ...models import Buschenschank

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

ENDPOINT = 'https://overpass-api.de/api/interpreter'

BBOX = (45, 5, 54.2, 18.25)
BUSCHENSCHANK_QUERY = """
    (
        node["cuisine"~"buschenschank"]{bbox};
        way["cuisine"~"buschenschank"]{bbox};
        relation["cuisine"~"buschenschank"]{bbox};
        node["cuisine"~"heuriger"]{bbox};
        way["cuisine"~"heuriger"]{bbox};
        relation["cuisine"~"heuriger"]{bbox};
    );
    out center meta;
""".format(bbox='').replace('\n', '')
#(bbox='(45.0,5.0,54.2,18.25)')
# bbox cause time out for whatever reason


class BuschenschankSaxParser(NodeCenterSaxParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new = 0
        self.updated = 0

    def process_item(self, element):
        osm_id = element['id']
        tags = element['tags']
        name = tags.get('name')

        if name is None:
            logger.warn('Nameless node found: %d' % osm_id)
            return False
        elif name == 'Heuriger':
            logger.warn('Badly named node: %d' % osm_id)

        if tags.get('disused', None) == 'yes':
            b = Buschenschank.objects.filter(is_removed=False, osm_id=osm_id).first()
            if b is not None:
                logger.info('Delete disused: %s', name)
                b.delete()
            else:
                logger.info('Skip disused: %s', name)
            return False

        lat = element['lat']
        lon = element['lon']
        if BBOX[0] <= lat <= BBOX[2] and BBOX[1] <= lon <= BBOX[3]:
            buschenschank = Buschenschank.objects.filter(osm_id=osm_id).first()
            if buschenschank is None:
                logger.info('New Buschenschank found: {tags[name]}'.format(**element))
                buschenschank = Buschenschank(osm_id=osm_id)
            elif buschenschank.modified < element['timestamp']:
                logger.info(
                    'Updated Buschenschank found: {tags[name]} by {user}'.format(**element)
                )

            buschenschank.name = name
            buschenschank.coordinates = Point(float(lon), float(lat))
            buschenschank.tags = tags
            buschenschank.save()


class Command(BaseCommand):
    help = 'Import Buschenschank/Heuriger from OSM'

    def handle(self, *args, **options):
        response = requests.post(
            ENDPOINT, data={'data': BUSCHENSCHANK_QUERY},
            headers={'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}
        )
        if response.ok:
            parseString(response.text, BuschenschankSaxParser())
        else:
            logger.error('Not possible to get XML: %d' % response.status_code)
