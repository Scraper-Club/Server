from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from core.models import ScrapComplainModel
from core.models import UrlPool
from core.proxies import Domain, Device, Url, Scrap, IPAddress, TokenRuleChain
from django.db.models import Q


class Scraper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.PositiveIntegerField(default=0)
    scrapes = models.PositiveIntegerField(default=0)
    complains = models.PositiveIntegerField(default=0)

    last_scrap = models.DateTimeField(null=True)
    allow_private = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    def get_domains(self):
        return Domain.objects.filter(owner=self.user)

    def get_devices(self):
        return Device.objects.filter(current_owner=self.user)

    def get_scrapes(self):
        return Scrap.objects.filter(owner=self.user).order_by('-upload_date')

    def get_ip_addresses(self):
        ips = self.get_devices() \
            .values_list('used_ip_addresses', flat=True).distinct() \
            .exclude(used_ip_addresses__isnull=True)

        return IPAddress.objects.filter(ip_address__in=ips)

    def get_available_for_scraping(self):
        return Url.objects.filter(Q(pool=UrlPool.PUBLIC) | Q(owner=self.user))

    def get_urls(self):
        return Url.objects.filter(owner=self.user)

    def get_public_urls(self):
        return Url.public_pool.filter(owner=self.user)

    def get_private_urls(self):
        return Url.private_pool.filter(owner=self.user)

    def get_waiting_urls(self):
        return Url.waiting_pool.filter(owner=self.user)

    def get_complains_send(self):
        return ScrapComplainModel.objects.filter(from_user=self.user)

    def get_complains_received(self):
        return ScrapComplainModel.objects.filter(on_user=self.user)

    def revoke_token(self, save=True):
        if self.tokens > 0:
            self.tokens -= 1
            if save:
                self.save()
            return True
        else:
            return False

    def add_token(self, count=1, save=True):
        if count > 0:
            self.tokens += count
            if save:
                self.save()
            return True
        else:
            return False

    def set_tokens(self, amount=0, save=True):
        if amount >= 0:
            self.tokens = amount
            if save:
                self.save()
            return True
        else:
            return False

    def add_scrap(self, url, save=True):
        self.scrapes += 1
        if url.pool == UrlPool.PUBLIC and url.owner != self.user:
            rule_chain = TokenRuleChain.objects.get(pk=1)
            if rule_chain.receive_token(self.scrapes):
                self.add_token(save=False)

        if save:
            self.save()

    def get_api_key(self):
        token, created = Token.objects.get_or_create(user=self.user)
        if created:
            token.save()
        return token

    def add_complain(self, save=True):
        self.revoke_token(save=False)
        self.complains += 1
        if save:
            self.save()

    def delete_public_pool(self, scraping=True):
        self.get_public_urls().scraped().delete()
        if scraping:
            tokens_count = self.get_public_urls().not_scraped_yet().count()
            self.get_public_urls().not_scraped_yet().delete()
        else:
            tokens_count = self.get_public_urls().available_for_scraping().count()
            self.get_public_urls().available_for_scraping().delete()

        self.add_token(count=tokens_count)

    def delete_private_pool(self, scraping=True):
        if scraping:
            self.get_private_urls().delete()
        else:
            self.get_public_urls().available_for_scraping().delete()
            self.get_public_urls().scraped().delete()

    def delete_urls(self, scraping=True):
        self.delete_private_pool(scraping)
        self.delete_public_pool(scraping)
