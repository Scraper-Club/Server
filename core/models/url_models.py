from django.db import models
from django.contrib.auth.models import User


class UrlStatus:
    NOT_SCRAPED = 'no'
    SCRAPING = 'in'
    SCRAPED = 'do'

    CHOICES = (
        (NOT_SCRAPED, 'Not scraped'),
        (SCRAPING, 'Scraping in progress'),
        (SCRAPED, 'Already scraped'),
    )


class UrlPool:
    PUBLIC = 'pub'
    PRIVATE = 'priv'
    WAITING = 'wait'

    CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (WAITING, 'Waiting')
    )


class UrlModel(models.Model):
    url = models.URLField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.ForeignKey('core.DomainModel', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=UrlStatus.CHOICES,
        default=UrlStatus.NOT_SCRAPED)
    pool = models.CharField(
        max_length=4,
        choices=UrlPool.CHOICES,
        default=UrlPool.WAITING,
    )
    configuration = models.ForeignKey('core.ConfigurationModel', on_delete=models.SET_NULL, null=True, default=None)
    scrap_start_time = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.url


class ConfigurationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wait_time = models.PositiveIntegerField(default=3)
    scroll_count = models.PositiveIntegerField(default=1)
    scroll_delay = models.PositiveIntegerField(default=1)
