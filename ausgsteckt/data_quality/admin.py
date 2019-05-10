from django.contrib import admin

from .models import PageCheckResult


@admin.register(PageCheckResult)
class PageCheckResultAdmin(admin.ModelAdmin):
    list_display = ('buschenschank', 'created', 'tag_name',
                    'website', 'return_code')
    list_filter = ('created', 'return_code', 'tag_name')
    search_fields = ('buschenschank__name', 'website')
