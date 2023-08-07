from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld
from django.contrib.flatpages.models import FlatPage


class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget(config_name="flatpage"))

    class Meta(FlatpageFormOld.Meta):
        pass


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
