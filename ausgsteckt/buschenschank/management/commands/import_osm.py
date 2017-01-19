import logging
from xml.sax import parseString

import requests

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.conf import settings

from ..utils.overpass_parser import NodeCenterSaxParser
from ...models import Buschenschank

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class BuschenschankSaxParser(NodeCenterSaxParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new = 0
        self.updated = 0
        self.skipped = 0
        self.amount = 0
        self.processed_ids = []

    def process_item(self, element):
        lat = element['lat']
        lon = element['lon']
        osm_id = element['id']
        osm_type = element['type']
        tags = element['tags']
        name = tags.get('name')
        self.amount += 1

        if name is None:
            logger.warning('Skip nameless %s: %d', osm_type, osm_id)
            self.skipped += 1
            return False
        elif name in ['Heuriger', 'Buschenschank']:
            logger.warning('Badly named %s: %d', osm_type, osm_id)

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
            self.processed_ids.append(buschenschank.id)
            return False

        name_len = Buschenschank._meta.get_field('name').max_length
        buschenschank.name = name[:name_len]
        buschenschank.coordinates = Point(float(lon), float(lat))
        modified_by_len = Buschenschank._meta.get_field('modified_by').max_length
        buschenschank.modified_by = element['user'][:modified_by_len]
        buschenschank.modified = element['timestamp']
        buschenschank.tags = tags
        buschenschank.save()
        self.processed_ids.append(buschenschank.id)


class Command(BaseCommand):
    help = 'Import Buschenschank/Heuriger from OSM'

    def check_removed(self, processed_ids):
        obsoletes = Buschenschank.objects.exclude(id__in=processed_ids)
        for obsolete in obsoletes:
            logger.warning(
                'Removed Buschenschank found: [%s/%d] %s',
                obsolete.osm_type, obsolete.osm_id, obsolete.name
            )
        if obsoletes.count() < 5:
            obsoletes.update(is_removed=True)
        else:
            logger.warning(
                'Unusual amount of deleted OSM elements: %d objects deleted, '
                'skipping mark as removed step',
                obsoletes.count()
            )

    def handle(self, *args, **options):
        response = requests.post(
            settings.OVERPASS_ENDPOINT, data={'data': settings.BUSCHENSCHANK_QUERY},
            headers={'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}
        )
        if response.ok:
            parser = BuschenschankSaxParser()
            parseString(response.text, parser)
            self.check_removed(parser.processed_ids)
            logger.info(
                'Import finished: '
                '{new} added, {updated} updated, '
                '{skipped} skipped (of {amount})'.format(
                    new=parser.new, updated=parser.updated,
                    skipped=parser.skipped, amount=parser.amount
                )
            )

        else:
            logger.error('Not possible to get XML: %d' % response.status_code)
