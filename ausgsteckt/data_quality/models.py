from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel

from buschenschank.models import Buschenschank


class PageCheckResult(TimeStampedModel):
    buschenschank = models.ForeignKey(
        Buschenschank, verbose_name=_('Buschenschank'),
        on_delete=models.SET_NULL, null=True)
    tag_name = models.CharField(max_length=255)
    website = models.CharField(
        _('Website URL'), help_text=_('URL checked'),
        max_length=255)
    return_code = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = _('Page check result')
        verbose_name_plural = _('Page check results')
