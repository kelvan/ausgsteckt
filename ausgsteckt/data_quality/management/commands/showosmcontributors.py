import logging
import operator
from xml.sax import parseString

import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from buschenschank.management.utils.overpass_parser import NodeCenterSaxParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class BuschenschankSaxParser(NodeCenterSaxParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = {}

    def process_item(self, element):
        user = element['user']
        self.users[user] = self.users.get(user, 0) + 1


class Command(BaseCommand):
    help = 'Extract active OSM contributors editing Buschenschank/Heuriger nodes'  # NOQA: E501

    def add_arguments(self, parser):
        parser.add_argument(
            '--min', dest='min', default='5',
            help='Only show contributors with at least <min> edits',
        )

    def handle(self, *args, **options):
        if options.get('min').isdigit():
            min_contrib = int(options['min'])
        else:
            min_contrib = 5

        response = requests.post(
            settings.OVERPASS_ENDPOINT,
            data={'data': settings.BUSCHENSCHANK_QUERY},
            headers={'Accept-Charset': 'utf-8;q=0.7,*;q=0.7'}
        )
        if response.ok:
            parser = BuschenschankSaxParser()
            parseString(response.text, parser)
            sorted_items = sorted(
                parser.users.items(), key=operator.itemgetter(1), reverse=True)
            for user, count in sorted_items:
                if count >= min_contrib:
                    print('%s: %d' % (user, count))
        else:
            logger.error('Not possible to get XML: %d' % response.status_code)
