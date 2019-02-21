from core.models import IPRateRule
from core.models.domain_models import DomainModel


class Domain(DomainModel):
    class Meta:
        proxy = True

    def reset_config(self, save=True):
        conf = self.configuration
        conf.wait_time = 3
        conf.scroll_count = 1
        conf.scroll_delay = 1
        if save:
            conf.save()

    def get_ip_rate_rule(self):
        if not self.ip_rate_rule:
            self.ip_rate_rule = IPRateRule.objects.create()
            self.save()
        return self.ip_rate_rule