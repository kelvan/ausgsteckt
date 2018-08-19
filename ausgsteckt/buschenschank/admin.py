from django.contrib.gis import admin as gis_admin
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from .models import Buschenschank, Region, Commune, OpenDate


class OpenTodayListFilter(admin.SimpleListFilter):
    title = _('Open today')

    parameter_name = 'open_today'

    def lookups(self, request, model_admin):
        return (('open', _('Open')),)

    def queryset(self, request, queryset):
        if self.value() == 'open':
            today = timezone.now().today()
            return queryset.filter(opendate__date_start__lte=today, opendate__date_end__gte=today)


class OpenDateInline(admin.TabularInline):
    model = OpenDate
    extra = 1


@admin.register(Buschenschank)
class BuschenschankAdmin(gis_admin.OSMGeoAdmin):
    openlayers_url = '//openlayers.org/api/2.13.1/OpenLayers.js'
    list_display = (
        'name', 'cuisine', 'latitude', 'longitude',
        'address', 'website_link', 'active',
        'modified_by', 'created', 'modified'
    )
    readonly_fields = ('osm_id', 'osm_type', 'is_removed')
    list_filter = ('is_removed', OpenTodayListFilter, 'created', 'modified', 'modified_by')
    search_fields = ('name', 'tags')

    inlines = [OpenDateInline]

    def active(self, instance):
        return not instance.is_removed
    active.boolean = True

    def website_link(self, instance):
        if instance.website:
            return format_html('<a href="{url}">{url}</a>', url=instance.website)

    def cuisine(self, instance):
        return instance.tags.get('cuisine')

    def get_queryset(self, request):
        qs = self.model.all.get_queryset()

        ordering = self.ordering or ()
        qs = qs.order_by(*ordering)
        return qs


@admin.register(Region)
class RegionAdmin(gis_admin.OSMGeoAdmin):
    openlayers_url = '//openlayers.org/api/2.13.1/OpenLayers.js'
    list_display = (
        'name', 'is_removed', 'published', 'website_link', 'created',
        'modified', 'buschenschank_count'
    )
    readonly_fields = ('osm_id', 'osm_type', 'is_removed')
    list_filter = ('is_removed', 'published', 'created', 'modified')
    search_fields = ('name', 'description', 'notes')
    save_on_top = True

    def website_link(self, instance):
        if instance.website:
            return format_html('<a target="_blank" href="{url}">{url}</a>', url=instance.website)

    def buschenschank_count(self, instance):
        return instance.get_buschenschank().count()


@admin.register(Commune)
class CommuneAdmin(gis_admin.OSMGeoAdmin):
    openlayers_url = '//openlayers.org/api/2.13.1/OpenLayers.js'
    list_display = (
        'name', 'district', 'county', 'is_removed', 'created', 'modified',
        'buschenschank_count'
    )
    readonly_fields = (
        'name', 'district', 'county', 'is_removed', 'created', 'modified'
    )
    list_filter = ('is_removed', 'county', 'created', 'modified')
    search_fields = ('name', 'district')
    actions = ['create_update_region']

    def buschenschank_count(self, instance):
        return instance.get_buschenschank().count()

    def create_update_region(self, request, queryset):
        created = 0
        updated = 0
        for commune in queryset:
            defaults = {'areas': commune.mpoly}
            obj, new = Region.objects.update_or_create(name=commune.name, defaults=defaults)
            if new:
                created += 1
            else:
                updated += 1
        self.message_user(
            request, _(
                '{created_count}/{updated_count} regions created/updated'
            ).format(
                created_count=created, updated_count=updated
            )
        )
    create_update_region.short_description = _(
        'Generate/update region with commune info'
    )


@admin.register(OpenDate)
class OpenDateAdmin(admin.ModelAdmin):
    list_display = ('buschenschank', 'date_start', 'date_end')
