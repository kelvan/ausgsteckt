import logging
from xml.sax import parseString

import requests

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ..utils.overpass_parser import NodeCenterSaxParser
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
    area["name"="Österreich"]->.boundaryarea;
    (
        node(area.boundaryarea)["cuisine"~"buschenschank"];
        way(area.boundaryarea)["cuisine"~"buschenschank"];
        relation(area.boundaryarea)["cuisine"~"buschenschank"];
        node(area.boundaryarea)["cuisine"~"heuriger"];
        way(area.boundaryarea)["cuisine"~"heuriger"];
        relation(area.boundaryarea)["cuisine"~"heuriger"];
    );
    out center meta;
""".replace('\n', '')


class BuschenschankSaxParser(NodeCenterSaxParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new = 0
        self.updated = 0
        self.skipped = 0
        self.amount = 0

    def process_item(self, element):
        lat = element['lat']
        lon = element['lon']
        osm_id = element['id']
        osm_type = element['type']
        tags = element['tags']
        name = tags.get('name')
        self.amount += 1
        if name is None:
            logger.warn('Skip nameless %s: %d', osm_type, osm_id)
            self.skipped += 1
            return False
        elif name in ['Heuriger', 'Buschenschank']:
            logger.warn('Badly named %s: %d', osm_type, osm_id)

        if tags.get('disused', None) == 'yes':
            b = Buschenschank.objects.filter(
                is_removed=False, osm_id=osm_id, osm_type=osm_type
            ).first()
            if b is not None:
                logger.info('Delete disused: %s', name)
                b.delete()
            else:
                logger.info('Skip disused: %s', name)
            self.skipped += 1
            return False

        buschenschank = Buschenschank.objects.filter(
            osm_id=osm_id, osm_type=osm_type
        ).first()
        if buschenschank is None:
            logger.info(
                'New Buschenschank found: {tags[name]} by {user}'.format(**element)
            )
            buschenschank = Buschenschank(osm_id=osm_id, osm_type=osm_type)
            self.new += 1
        elif buschenschank.modified < element['timestamp']:
            logger.info(
                'Updated Buschenschank found: {tags[name]} by {user}'.format(**element)
            )
            self.updated += 1
        else:
            return False

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
            parser = BuschenschankSaxParser()
            parseString(response.text, parser)
            logger.info(
                'Import finished: {new} added, {updated} updated, {skipped} skipped (of {amount})'.format(
                    new=parser.new, updated=parser.updated,
                    skipped=parser.skipped, amount=parser.amount
                )
            )
        else:
            logger.error('Not possible to get XML: %d' % response.status_code)
