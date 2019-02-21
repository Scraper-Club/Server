from core.models import IPAddressModel, IPRate
from .IPConnection import IPConnection


class IPAddress(IPAddressModel):
    class Meta:
        proxy = True

    def get_last_hour_connections(self, domain=None):
        if domain:
            return IPConnection.hourly.filter(ip_address=self, domain=domain)
        else:
            return IPConnection.hourly.filter(ip_address=self)

    def get_last_day_connections(self, domain=None):
        if domain:
            return IPConnection.daily.filter(ip_address=self, domain=domain)
        else:
            return IPConnection.daily.filter(ip_address=self)

    def get_last_connection(self):
        return IPConnection.objects.filter(ip_address=self).order_by('-time')[:1]

    def is_over_limit(self):
        if self.rate_type == IPRate.UNLIMITED:
            return False
        elif self.rate_type == IPRate.PER_HOUR:
            return self.get_last_hour_connections().count() >= self.rate_limit
        elif self.rate_type == IPRate.PER_DAY:
            return self.get_last_day_connections().count() >= self.rate_limit

    def on_domain_connected(self, domain):
        IPConnection.objects.create(ip_address=self, domain=domain)

    def is_unlimited(self):
        return self.rate_type == IPRate.UNLIMITED
