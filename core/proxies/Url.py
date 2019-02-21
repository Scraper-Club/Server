from datetime import datetime, timedelta

from django.db import models

from core.models import UrlModel, UrlStatus, UrlPool
from .Scrap import Scrap


class UrlQuerySet(models.QuerySet):
    def not_scraped_yet(self):
        return self.exclude(status=UrlStatus.SCRAPED)

    def scraped(self):
        return self.filter(status=UrlStatus.SCRAPED)

    def available_for_scraping(self, device=None, ip_address=None):
        query_set = self.filter(status=UrlStatus.NOT_SCRAPED)
        if ip_address:
            if ip_address.is_over_limit():
                return query_set.none()
            query_set = query_set.exclude(domain__blacklist__ip_addresses__exact=ip_address)
        if device:
            query_set = query_set.exclude(domain__blacklist__devices__exact=device)
        return query_set

    def scraping(self):
        return self.filter(status=UrlStatus.SCRAPING)


class UrlManager(models.Manager):
    def get_queryset(self):
        return UrlQuerySet(self.model, using=self._db)

    def not_scraped_yet(self):
        return self.get_queryset().not_scraped_yet()

    def scraped(self):
        return self.get_queryset().scraped()

    def available_for_scraping(self, device=None, ip_address=None):
        return self.get_queryset().available_for_scraping(device, ip_address)

    def scraping(self):
        return self.get_queryset().scraping()

    def refresh_scraping(self, minutes=5):
        time_threshold = datetime.now() - timedelta(minutes=minutes)
        self.filter(scrap_start_time__lt=time_threshold, status=UrlStatus.SCRAPING).update(status=UrlStatus.NOT_SCRAPED)


class PublicPoolUrlManager(UrlManager):
    def get_queryset(self):
        return UrlQuerySet(self.model, using=self._db).filter(pool=UrlPool.PUBLIC)


class PrivatePoolUrlManager(UrlManager):
    def get_queryset(self):
        return UrlQuerySet(self.model, using=self._db).filter(pool=UrlPool.PRIVATE)


class WaitingPoolUrlManager(UrlManager):
    def get_queryset(self):
        return UrlQuerySet(self.model, using=self._db).filter(pool=UrlPool.WAITING)


class Url(UrlModel):
    objects = UrlManager()
    private_pool = PrivatePoolUrlManager()
    public_pool = PublicPoolUrlManager()
    waiting_pool = WaitingPoolUrlManager()

    class Meta:
        proxy = True

    def get_current_config(self):
        if self.configuration:
            return self.configuration
        else:
            return None

    def move(self, pool, save=True):
        print('Moving ' + str(self) + ' from ' + self.get_pool_display() + ' to ' + str(pool))
        if self.pool != pool and self.status == UrlStatus.NOT_SCRAPED:
            self.pool = pool
            if save:
                self.save()
            return True
        else:
            return False

    def move_to_public(self, save=True):
        return self.move(UrlPool.PUBLIC, save)

    def move_to_waiting(self, save=True):
        return self.move(UrlPool.WAITING, save)

    def move_to_private(self, save=True):
        return self.move(UrlPool.PRIVATE, save)

    def get_configuration(self):
        if self.configuration:
            return self.configuration
        else:
            return self.domain.configuration

    def on_scrap_started(self, save=True):
        self.status = UrlStatus.SCRAPING
        self.scrap_start_time = datetime.now()
        if save:
            self.save()

    def get_scrap_id(self):
        try:
            return Scrap.objects.get(url=self).id
        except Scrap.DoesNotExist:
            return None

    def is_scraped(self):
        return self.status == UrlStatus.SCRAPED
