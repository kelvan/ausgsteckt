import os

import wikipedia
import requests

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.measure import Distance as D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

from model_utils.models import TimeStampedModel, SoftDeletableModel
from easy_thumbnails.fields import ThumbnailerImageField

OSMTYPES = (
    ('node', _('Node')),
    ('way', _('Way')),
    ('relation', _('Relation'))
)

WIKIPEDIA_CITE = '-- https://{lang}.wikipedia.org/wiki/{page} (CC by-sa)'


class AdminURLMixin:
    def get_admin_url(self):
        return reverse('admin:{0}_{1}_change'.format(
            self._meta.app_label, self._meta.model_name), args=(self.pk,)
        )


class PublicManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)


class OSMItemModel(models.Model):
    osm_id = models.BigIntegerField(_('OSM ID'), blank=True, null=True)
    osm_type = models.CharField(
        _('OSM Type'), blank=True, null=True, max_length=8, choices=OSMTYPES
    )

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    published = models.BooleanField(_('Published'), default=True)

    public = PublicManager()

    class Meta:
        abstract = True


class Buschenschank(OSMItemModel, TimeStampedModel, SoftDeletableModel,
                    PublishableModel, AdminURLMixin):
    name = models.CharField(_('Name'), max_length=50)
    coordinates = models.PointField(_('Coordinates'))
    modified_by = models.CharField(
        _('Last edit OSM user'), max_length=50, blank=True, null=True
    )
    tags = JSONField(_('Tags'), blank=True, null=True)

    # include removed objects
    all = models.Manager()

    @property
    def slug(self):
        return slugify(self.name)

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
        website = self.tags.get('website') or self.tags.get('contact:website')
        if website and not website.startswith('http'):
            website = 'http://' + website
        return website

    @property
    def phone(self):
        return self.tags.get('contact:phone') or self.tags.get('phone')

    @property
    def email(self):
        return self.tags.get('contact:email') or self.tags.get('email')

    @cached_property
    def region(self):
        return Region.objects.filter(areas__contains=self.coordinates).first()

    def get_nearby(self, distance_km=1.5):
        nearby = Buschenschank.objects.exclude(pk=self.pk).annotate(
            distance=Distance('coordinates', self.coordinates)
        ).order_by('distance')
        nearby = nearby.filter(distance__lte=D(km=distance_km))
        return nearby

    def get_osm_url(self):
        return 'https://openstreetmap.org/%s/%d' % (self.osm_type, self.osm_id)

    def get_map_permalink(self):
        return '{baseUrl}#lat={buschenschank.latitude}&lon={buschenschank.longitude}&zoom={zoom}&layer={layer}'.format(
            baseUrl=reverse('buschenschank:buschenschank_map'), buschenschank=self, zoom=18, layer='OpenStreetMap')

    def get_absolute_url(self):
        return reverse('buschenschank:buschenschank_details', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Buschenschank'
        verbose_name_plural = 'Buschenschanken'
        ordering = ('name',)


class Region(OSMItemModel, TimeStampedModel, SoftDeletableModel,
             PublishableModel, AdminURLMixin):
    name = models.CharField(_('Name'), max_length=50)
    description = models.TextField(
        _('Description'), help_text=_('Description shown on region page'),
        blank=True, null=True
    )
    wikipedia_page = models.CharField(
        _('Wikipedia page'), max_length=50, blank=True, null=True,
        help_text=_('Used to load description if none set')
    )
    region_image = ThumbnailerImageField(
        _('Region image'),
        help_text=_('Image displayed on region page'),
        upload_to='images/regions', blank=True
    )
    areas = models.MultiPolygonField(_('Areas'))
    website = models.URLField(_('Website'), blank=True, null=True)
    calendar_website = models.URLField(
        _('Calendar website'), blank=True, null=True
    )
    keywords = models.CharField(
        _('Keywords'), blank=True, null=True, max_length=255
    )
    notes = models.TextField(
        _('Notes'), help_text=_('Internal notes'),
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    @property
    def slug(self):
        return slugify(self.name)

    def load_image_from_web(self, url):
        r = requests.get(url)
        rel_path = os.path.join(self.__class__.region_image.field.upload_to, os.path.basename(url))
        target_file = os.path.join(settings.MEDIA_ROOT, rel_path)

        with open(target_file, 'wb') as f:
            f.write(r.content)
        self.region_image.name = rel_path
        self.save()

    def save(self, **kwargs):
        if self.wikipedia_page:
            lang = settings.LANGUAGE_CODE[:2]
            wikipedia.set_lang(lang)
            wp_page = wikipedia.page(self.wikipedia_page)

            if not self.description:
                self.description = wp_page.summary
                self.description += '\n' + WIKIPEDIA_CITE.format(page=self.wikipedia_page, lang=lang)
            if not self.region_image.name:
                COA_FILENAME_CONTENT = ['coa', 'wappen']
                for image in wp_page.images:
                    matches = [m in image.lower() for m in COA_FILENAME_CONTENT]
                    if any(matches) and self.name.split()[0].lower() in image.lower():
                        self.load_image_from_web(image)
                        break

        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('buschenschank:region_details', kwargs={'pk': self.pk, 'slug': self.slug})

    def get_buschenschank(self):
        return Buschenschank.objects.filter(coordinates__intersects=self.areas)

    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ('name',)


class Commune(TimeStampedModel, SoftDeletableModel):
    name = models.CharField(_('Name'), max_length=100)
    district = models.CharField(_('District'), max_length=100)
    county = models.CharField(_('County'), max_length=20)
    mpoly = models.MultiPolygonField(_('Multipolygon'))

    def __str__(self):
        return self.name

    def get_buschenschank(self):
        return Buschenschank.objects.filter(coordinates__intersects=self.mpoly)

    class Meta:
        verbose_name = _('Commune')
        verbose_name_plural = _('Communes')
        unique_together = ('name', 'district', 'county')
