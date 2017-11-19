import logging

from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping

from ...models import Commune

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# AT Communes OpenData
# https://www.data.gv.at/katalog/dataset/c33d36b0-f184-4f2a-89cc-839ca7fcf88a


class Command(BaseCommand):
    help = 'Import Communes from shapefile (e.g. OpenData)'

    def add_arguments(self, parser):
        parser.add_argument('shapefile')

    def handle(self, *args, **options):
        mapping = {
            'name': 'Gem_Name', 'district': 'Bez_Name', 'county': 'Land_Name',
            'mpoly': 'POLYGON'
        }
        lm = LayerMapping(
            Commune, options['shapefile'], mapping,
            unique=('name', 'district', 'county')
        )
        lm.save(progress=100)
