from django.contrib.gis import admin

from .models import Buschenschank


@admin.register(Buschenschank)
class BuschenschankAdmin(admin.GeoModelAdmin):
    list_display = ('name', 'cuisine', 'latitude', 'longitude')
    search_fields = ('name',)
    
    def cuisine(self, instance):
        return instance.tags.get('cuisine')
