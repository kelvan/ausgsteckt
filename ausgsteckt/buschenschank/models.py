from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel, SoftDeletableModel
from easy_thumbnails.fields import ThumbnailerImageField

OSMTYPES = (
    ('node', _('Node')),
    ('way', _('Way')),
    ('relation', _('Relation'))
)

class AdminURLMixin:
    def get_admin_url(self):
        return reverse('admin:{0}_{1}_change'.format(self._meta.app_label, self._meta.model_name), args=(self.pk,))


class PublicManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)


class PublishableModel(models.Model):
    published = models.BooleanField(default=True)

    public = PublicManager()

    class Meta:
        abstract = True


class Buschenschank(TimeStampedModel, SoftDeletableModel, PublishableModel, AdminURLMixin):
    name = models.CharField(max_length=50)
    coordinates = models.PointField()
    osm_id = models.BigIntegerField(blank=True, null=True)
    osm_type = models.CharField(
        blank=True, null=True, max_length=8, choices=OSMTYPES
    )
    tags = JSONField(blank=True, null=True)

    #objects = models.GeoManager()
    # TODO add manager for undeleted

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
    def opening_hours(self):
        return self.tags.get('opening_hours')

    @property
    def opening_hours_url(self):
        return self.tags.get('opening_hours:url')

    @property
    def website(self):
        return self.tags.get('website') or self.tags.get('contact:website')

    @property
    def phone(self):
        return self.tags.get('contact:phone') or self.tags.get('phone')

    @property
    def email(self):
        return self.tags.get('contact:email') or self.tags.get('email')

    def get_osm_url(self):
        # XXX should be https but iD editor breaks on https due mixed content
        return 'http://openstreetmap.org/%s/%d' % (self.osm_type, self.osm_id)

    def get_absolute_url(self):
        return self.get_osm_url()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Buschenschank'
        verbose_name_plural = 'Buschenschänke'


class Region(TimeStampedModel, SoftDeletableModel, PublishableModel):
    name = models.CharField(max_length=50)
    description = models.TextField(
        _('Description'), help_text=_('Description shown on region page'),
        blank=True, null=True
    )
    region_image = ThumbnailerImageField(
        _('Region image'),
        help_text=_('Image displayed on region page'),
        upload_to='images/regions', blank=True
    )
    areas = models.MultiPolygonField()
    website = models.URLField(blank=True, null=True)
    calendar_website = models.URLField(blank=True, null=True)
    keywords = models.CharField(blank=True, null=True, max_length=255)
    notes = models.TextField(
        _('Notes'), help_text=_('Internal notes'),
        blank=True, null=True
    )

    def __str__(self):
        return self.name
