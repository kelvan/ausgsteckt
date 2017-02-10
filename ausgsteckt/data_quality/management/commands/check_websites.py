import csv
import logging
import itertools
import asyncio
import async_timeout

from aiohttp import ClientSession

from django.core.management.base import BaseCommand

from buschenschank.models import Buschenschank

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return response


async def check_url(session, buschenschank, tag_key):
    errors = []
    url = buschenschank.tags.get(tag_key)
    if url:
        error = {
            'id': buschenschank.id, 'buschenschank_name': buschenschank.name,
            'url': url, 'tag_key': tag_key, 'error': '',
            'status_code': '', 'osm_url': buschenschank.get_osm_url()
        }
        if not url.startswith('http'):
            logger.error(
                'InvalidURL: %s -> %s: %s', buschenschank.name,
                tag_key, url
            )
            new_error = dict(**error)
            new_error['error'] = 'InvalidURL'
            errors.append(new_error)
            url = 'http://' + url
            error['url'] = url
            logger.info('Replaced url with: %s', url)
        try:
            r = await fetch(session, url)
            if not r.status == 200:
                logger.warning(
                    '[%s] %s -> %s', r.status,
                    buschenschank.name, tag_key
                )
                error['status_code'] = r.status
                errors.append(error)
        except Exception as e:
            logger.error(
                '%s -> %s: [%s] %s', buschenschank.name, tag_key, e.__class__, e
            )
            error['error'] = e
            errors.append(error)
    return errors


class Command(BaseCommand):
    help = 'Check Buschenschank websites'

    def add_arguments(self, parser):
        parser.add_argument(
            '--report', dest='report', help='Save report as csv'
        )

    def _save_report(self, errors, report_path):
        with open(report_path, 'w') as csvfile:
            fieldnames = [
                'id', 'buschenschank_name', 'tag_key', 'url', 'status_code',
                'error', 'osm_url'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(errors)

    async def _checker(self):
        async with ClientSession() as session:
            tasks = []
            for buschenschank in self.queryset:
                for key in self.webkeys:
                    tasks.append(check_url(session, buschenschank, key))

            errors = await asyncio.gather(*tasks)
            errors = list(itertools.chain.from_iterable(errors))
            logger.info('Errors: %d', len(errors))

        if self.report_path:
            self._save_report(errors, self.report_path)

    def handle(self, *args, **options):
        self.report_path = options.get('report')
        self.webkeys = ['website', 'contact:website', 'opening_hours:url']
        self.queryset = Buschenschank.objects.filter(
            tags__has_any_keys=self.webkeys
        )

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._checker())
        loop.run_until_complete(future)
