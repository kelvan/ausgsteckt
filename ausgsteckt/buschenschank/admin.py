from django.contrib.gis import admin
from django.utils.html import format_html

from .models import Buschenschank


@admin.register(Buschenschank)
class BuschenschankAdmin(admin.OSMGeoAdmin):
    list_display = (
        'name', 'active', 'cuisine', 'latitude', 'longitude', 'address',
        'website_link'
    )
    list_filter = ('is_removed',)
    search_fields = ('name', 'tags')
    
    def active(self, instance):
        return not instance.is_removed
    active.boolean = True

    def website_link(self, instance):
        if instance.website:
            return format_html('<a href="{url}">{url}</a>', url=instance.website)

    def cuisine(self, instance):
        return instance.tags.get('cuisine')
