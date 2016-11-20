import logging

import requests

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import MultiPolygon

from ...models import Region
from ..utils.polygon_helper import GeoJSONPolygonBuilder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

ENDPOINT = 'https://overpass-api.de/api/interpreter'

REGION_QUERY = """
    [out:json];
    (
        {osm_type}({osm_id});
    );
    out body;
    >;
    out skel qt;
""".replace('\n', '')


class Command(BaseCommand):
    help = 'Import Region from OSM'

    def add_arguments(self, parser):
        parser.add_argument('osm_type')
        parser.add_argument('osm_id', type=int)

    def handle(self, *args, **options):
        osm_types = ['way', 'relation']
        osm_id = options['osm_id']
        osm_type = options['osm_type']

        if osm_type not in osm_types:
            raise CommandError('Only %s allowed' % osm_types)

        query = REGION_QUERY.format(osm_type=osm_type, osm_id=osm_id)

        response = requests.post(
            ENDPOINT, data={'data': query},
            headers={'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}
        )
        if response.ok:
            defaults = {}
            region_json = response.json()
            defaults['name'] = region_json['elements'][0]['tags']['name']

            polygon_builder = GeoJSONPolygonBuilder(region_json['elements'])
            polygon_builder.prepare_data()
            polygon = polygon_builder.build_polygon()

            # TODO support relation with subrelations/ways as MultiPolygon
            defaults['areas'] = MultiPolygon(polygon)

            region, created = Region.objects.update_or_create(
                osm_type=osm_type, osm_id=osm_id, defaults=defaults
            )
        else:
            logger.error(
                'Not possible to get %s: %d', osm_type, response.status_code
            )
