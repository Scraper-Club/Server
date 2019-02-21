from django.db import models
from django.contrib.auth.models import User

from core.models import ConfigurationModel


class DomainModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=255)
    configuration = models.ForeignKey('core.ConfigurationModel', on_delete=models.SET_NULL, null=True, default=None)
    ip_rate_rule = models.ForeignKey('core.IPRateRule', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        unique_together = ('owner', 'hostname')

    def save(self, *args, **kwargs):
        if not self.pk:
            conf = ConfigurationModel.objects.create(user=self.owner)
            self.configuration = conf
            super(DomainModel, self).save(*args, **kwargs)
            BlackList.objects.create(domain=self)
        else:
            super(DomainModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.hostname


class BlackList(models.Model):
    domain = models.OneToOneField('core.DomainModel', on_delete=models.CASCADE)
    devices = models.ManyToManyField('core.DeviceModel')
    ip_addresses = models.ManyToManyField('core.IPAddressModel')

    def __str__(self):
        return str(self.domain) + ':' + str(self.domain.owner)
