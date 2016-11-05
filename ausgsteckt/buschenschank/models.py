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
    def place(self):
        return self.tags.get('addr:place')

    @property
    def housenumber(self):
        return self.tags.get('addr:housenumber')

    @property
    def address(self):
        if self.street or self.housenumber or self.postcode or self.city:
            addr = '%s %s, %s %s' % (
                self.street or self.place or '<street unknown>',
                self.housenumber or '<number unknown>',
                self.postcode or '<postcode unknown>',
                self.city or '<city unknown>'
            )
            if self.country:
                addr += ', ' + self.country
            return addr

    @property
    def website(self):
        return self.tags.get('website') or self.tags.get('contact:website')

    @property
    def phone(self):
        return self.tags.get('contact:phone') or self.tags.get('phone')

    @property
    def email(self):
        return self.tags.get('contact:email') or self.tags.get('email')

    def get_absolute_url(self):
        return 'https://openstreetmap.org/node/%d' % self.osm_id

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Buschenschank'
        verbose_name_plural = 'Buschenschänken'
