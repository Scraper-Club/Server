from datetime import datetime, timedelta

from django.db import models

from core.models import IPConnectionModel


class IPConnectionQuerySet(models.QuerySet):
    def refresh_connections(self):
        time_threshold = datetime.now() - timedelta(hours=24)
        return self.filter(time__lt=time_threshold).delete()


class IPConnectionsManager(models.Manager):
    def get_queryset(self):
        return IPConnectionQuerySet(self.model, using=self._db)

    def refresh_connections(self):
        return self.get_queryset().refresh_connections()


class DailyIPConnectionsManager(IPConnectionsManager):
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=24)
        return super().get_queryset().filter(time__gt=time_threshold)


class HourlyIPConnectionsManager(IPConnectionsManager):
    def get_queryset(self):
        time_threshold = datetime.now() - timedelta(hours=1)
        return super().get_queryset().filter(time__gt=time_threshold)


class IPConnection(IPConnectionModel):
    objects = IPConnectionsManager()
    daily = DailyIPConnectionsManager()
    hourly = HourlyIPConnectionsManager()

    class Meta:
        proxy = True