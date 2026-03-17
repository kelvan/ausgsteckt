import logging
from xml.sax import parseString

import requests
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from ...models import Buschenschank
from ..utils.overpass_parser import NodeCenterSaxParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
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

    def process_item(self, item):
        lat = item["lat"]
        lon = item["lon"]
        osm_id = item["id"]
        osm_type = item["type"]
        tags = item["tags"]
        name = tags.get("name")
        self.amount += 1

        if name is None:
            logger.warning("Skip nameless %s: %d", osm_type, osm_id)
            self.skipped += 1
            return False
        elif name in ["Heuriger", "Buschenschank"]:
            logger.warning("Badly named %s: %d", osm_type, osm_id)

        if tags.get("disused", None) == "yes":
            b = Buschenschank.objects.filter(is_removed=False, osm_id=osm_id, osm_type=osm_type).first()
            if b is not None:
                logger.info("Delete disused: %s", name)
                b.delete()
            else:
                logger.info("Skip disused: %s", name)
            self.skipped += 1
            return False

        buschenschank = Buschenschank.objects.filter(osm_id=osm_id, osm_type=osm_type).first()
        if buschenschank is None:
            logger.info("New Buschenschank found: {tags[name]} by {user}".format(**item))
            buschenschank = Buschenschank(osm_id=osm_id, osm_type=osm_type)
            self.new += 1
        elif buschenschank.modified < item["timestamp"]:  # ty:ignore[unresolved-attribute]
            logger.info("Updated Buschenschank found: {tags[name]} by {user}".format(**item))
            self.updated += 1
        else:
            self.processed_ids.append(buschenschank.id)  # ty:ignore[unresolved-attribute]
            return False

        name_len = Buschenschank._meta.get_field("name").max_length  # ty:ignore[unresolved-attribute]
        buschenschank.name = name[:name_len]  # ty:ignore[unresolved-attribute]
        buschenschank.coordinates = Point(float(lon), float(lat))  # ty:ignore[unresolved-attribute]
        modified_by_len = Buschenschank._meta.get_field("modified_by").max_length  # ty:ignore[unresolved-attribute]
        buschenschank.modified_by = item["user"][:modified_by_len]  # ty:ignore[unresolved-attribute]
        buschenschank.modified = item["timestamp"]  # ty:ignore[unresolved-attribute]
        buschenschank.tags = tags  # ty:ignore[unresolved-attribute]
        buschenschank.save()
        self.processed_ids.append(buschenschank.id)  # ty:ignore[unresolved-attribute]


class Command(BaseCommand):
    help = "Import Buschenschank/Heuriger from OSM"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force-delete",
            action="store_true",
            dest="force_delete",
            default=False,
            help="Delete objects even if unusual high amount",
        )

    def check_removed(self, processed_ids, force_delete=False):
        obsoletes = Buschenschank.objects.exclude(id__in=processed_ids)
        for obsolete in obsoletes:
            logger.warning(
                "Removed Buschenschank found: [%s/%d] %s",
                obsolete.osm_type,  # ty:ignore[unresolved-attribute]
                obsolete.osm_id,  # ty:ignore[unresolved-attribute]
                obsolete.name,  # ty:ignore[unresolved-attribute]
            )
        if obsoletes.count() < 20 or force_delete is True:
            obsoletes.update(is_removed=True)
        else:
            logger.warning(
                "Unusual amount of deleted OSM elements: %d objects deleted, skipping mark as removed step",
                obsoletes.count(),
            )

    def handle(self, *args, **options):
        response = requests.post(
            settings.OVERPASS_ENDPOINT,
            data={"data": settings.BUSCHENSCHANK_QUERY},
            headers={"Accept-Charset": "utf-8;q=0.7,*;q=0.7"},
        )
        if response.ok:
            parser = BuschenschankSaxParser()
            parseString(response.text, parser)
            self.check_removed(parser.processed_ids, force_delete=options["force_delete"])
            logger.info(
                "Import finished: "
                f"{parser.new} added, {parser.updated} updated, "
                f"{parser.skipped} skipped (of {parser.amount})"
            )

        else:
            logger.error(f"Not possible to get XML: {response.status_code}")
