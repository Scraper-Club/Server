from django.db import models
from django.contrib.auth.models import User


class IPRate:
    UNLIMITED = 'unlimited'
    PER_DAY = 'daily'
    PER_HOUR = 'hourly'

    CHOICES = (
        (UNLIMITED, 'Unlimited'),
        (PER_DAY, 'Per day'),
        (PER_HOUR, 'Per hour'),
    )


class IPRateRule(models.Model):
    rate_type = models.CharField(
        max_length=10,
        choices=IPRate.CHOICES,
        default=IPRate.UNLIMITED,
    )
    rate_limit = models.PositiveIntegerField(default=1000)


class IPAddressModel(models.Model):
    ip_address = models.GenericIPAddressField(primary_key=True)
    rate_type = models.CharField(
        max_length=10,
        choices=IPRate.CHOICES,
        default=IPRate.UNLIMITED,
    )
    rate_limit = models.PositiveIntegerField(default=1000)

    def __str__(self):
        return self.ip_address


class IPConnectionModel(models.Model):
    ip_address = models.ForeignKey('core.IPAddressModel', on_delete=models.CASCADE)
    domain = models.ForeignKey('core.DomainModel', null=True, on_delete=models.SET_NULL)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip_address} {self.domain} {self.time}'
