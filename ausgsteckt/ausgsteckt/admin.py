from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.forms import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage
from django_prose_editor.widgets import AdminProseEditorWidget


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=AdminProseEditorWidget())

    class Meta(FlatpageFormOld.Meta):
        pass


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
