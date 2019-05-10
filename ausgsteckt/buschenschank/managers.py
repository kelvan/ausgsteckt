from django.db import models
from django.utils import timezone


class OpenTodayManager(models.Manager):

    def get_queryset(self):
        today = timezone.now().date()
        return super().get_queryset().filter(
            opendate__date_start__lte=today, opendate__date_end__gte=today)
