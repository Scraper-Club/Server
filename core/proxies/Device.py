from datetime import datetime, timedelta

from core.models import DeviceModel, DeviceStatisticModel, ScrapModel
from .Url import Url


class Device(DeviceModel):
    class Meta:
        proxy = True

    def get_statistic(self):
        if self.current_owner:
            statistic, created = DeviceStatisticModel.objects.get_or_create(device=self, user=self.current_owner)
            if created:
                statistic.save()
        else:
            statistic = None
        return statistic

    def block(self, save=True):
        statistic = self.get_statistic()
        if statistic.is_blocked:
            return False
        else:
            statistic.is_blocked = True
            if save:
                statistic.save()
            return True

    def unblock(self, save=True):
        statistic = self.get_statistic()
        if not statistic.is_blocked:
            return False
        else:
            statistic.is_blocked = False
            if save:
                statistic.save()
            return True

    def add_ip_address(self, ip_address):
        self.used_ip_addresses.add(ip_address)

    def change_owner(self, new_owner, save=True):
        self.current_owner = new_owner
        if save:
            self.save()

    def add_scrap(self):
        statistic = self.get_statistic()
        statistic.scrapes_count += 1
        statistic.save()

    def add_complain(self, save=True):
        statistic = self.get_statistic()
        statistic.complains_count += 1
        if save:
            statistic.save()

    def get_public_urls(self, current_ip):
        statistic = self.get_statistic()
        if statistic.is_blocked:
            return Url.public_pool.none()

        return Url.public_pool.available_for_scraping(device=self, ip_address=current_ip)

    def get_waiting_urls(self, current_ip):
        statistic = self.get_statistic()
        if statistic.is_blocked:
            return Url.waiting_pool.none()

        return Url.waiting_pool.available_for_scraping(device=self, ip_address=current_ip).filter(owner__scraper__tokens__gt=0)

    def get_last_hour_scrapes(self):
        time_threshold = datetime.now() - timedelta(hours=1)
        return ScrapModel.objects.filter(
            scraper_device=self,
            scraper_user=self.current_owner,
            upload_date__gt=time_threshold
        )

    # TODO rename available into public
    def get_stats(self, current_ip):
        statistic = self.get_statistic()

        return {
            'available': self.get_public_urls(current_ip).union(self.get_waiting_urls(current_ip)).count(),
            'total_scrapes': statistic.scrapes_count,
            'complains': statistic.complains_count,
            'last_hour_scrapes': self.get_last_hour_scrapes().count(),
            'blocked': statistic.is_blocked,
            'ip': str(current_ip),
        }
