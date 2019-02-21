from django.db import models
from django.contrib.auth.models import User


class DeviceModel(models.Model):
    device_id = models.CharField(max_length=50, primary_key=True)
    vendor = models.CharField(max_length=30, default='vendor')
    model = models.CharField(max_length=30, default='model')
    android_version = models.CharField(max_length=10, default='android')

    current_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    used_ip_addresses = models.ManyToManyField('core.IPAddressModel')

    def __str__(self):
        return f"{self.vendor} {self.model} {self.android_version}"


class DeviceStatisticModel(models.Model):
    device = models.ForeignKey('core.DeviceModel', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scrapes_count = models.PositiveIntegerField(default=0)
    complains_count = models.PositiveIntegerField(default=0)
    is_blocked = models.BooleanField(default=False)