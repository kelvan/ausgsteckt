from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField

from model_utils.models import TimeStampedModel, SoftDeletableModel


class Buschenschank(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(max_length=50)
    coordinates = models.PointField()
    osm_id = models.BigIntegerField(blank=True, null=True)
    activated = models.BooleanField(default=False)
    tags = JSONField(blank=True, null=True)

    objects = models.GeoManager()

    @property
    def latitude(self):
        return self.coordinates.y

    @property
    def longitude(self):
        return self.coordinates.x

    @property
    def country(self):
        return self.tags.get('addr:country')

    @property
    def postcode(self):
        return self.tags.get('addr:postcode')

    @property
    def city(self):
        return self.tags.get('addr:city')

    @property
    def street(self):
        return self.tags.get('addr:street')

    @property
    def housenumber(self):
        return self.tags.get('addr:housenumber')

    @property
    def address(self):
        addr = '%s %s, %s %s' % (
            self.street or '<street unknown>',
            self.housenumber or '<number unknown>',
            self.postcode or '<postcode unknown>',
            self.city or '<city unknown>'
        )
        if self.country:
            addr += ', ' + self.country
        return addr

    @property
    def website(self):
        return self.tags.get('website')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Buschenschank'
        verbose_name_plural = 'Buschenschänken'
