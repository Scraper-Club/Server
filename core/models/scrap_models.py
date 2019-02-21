from django.db import models
from django.contrib.auth.models import User


class ScrapModel(models.Model):
    file = models.BinaryField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    url = models.ForeignKey('core.UrlModel', null=True, on_delete=models.SET_NULL)
    url_value = models.CharField(max_length=1000)
    scraper_user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL
    )
    scraper_device = models.ForeignKey(
        'core.DeviceModel', null=True, on_delete=models.SET_NULL
    )
    ip_address = models.ForeignKey('core.IPAddressModel', null=True, on_delete=models.SET_NULL)
    upload_date = models.DateTimeField(auto_now_add=True)
    complained = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.url_value = self.url.url
            self.owner = self.url.owner
            self.scraper_user = self.scraper_device.current_owner
        super(ScrapModel, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.url:
            self.url.delete()
        super(ScrapModel, self).delete(using, keep_parents)

    def __str__(self):
        return self.url_value


class ScrapComplainModel(models.Model):
    scrap = models.ForeignKey('core.ScrapModel', on_delete=models.SET_NULL, null=True)
    message = models.CharField(max_length=300, default='Bad scrap')
    time = models.DateTimeField(auto_now_add=True)
    on_device = models.ForeignKey(
        'core.DeviceModel', null=True, on_delete=models.SET_NULL
    )
    on_user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='receiver'
    )
    on_ip_address = models.ForeignKey(
        'core.IPAddressModel', null=True, on_delete=models.SET_NULL
    )
    from_user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='sender'
    )


class TokenRuleModel(models.Model):
    from_scrapes_count = models.IntegerField(default=0)
    to_scrapes_count = models.IntegerField(default=-1)
    scrapes_per_token = models.IntegerField(default=1)


class TokenRuleChainModel(models.Model):
    token_rules = models.ManyToManyField('core.TokenRuleModel')
