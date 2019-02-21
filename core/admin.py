from django.contrib import admin

from core.models import DeviceModel, Scraper, IPAddressModel, DomainModel, DeviceStatisticModel, IPRateRule, \
    IPConnectionModel, ScrapModel, ScrapComplainModel
from core.models.domain_models import BlackList

admin.site.register(DeviceModel)
admin.site.register(Scraper)
admin.site.register(IPAddressModel)
admin.site.register(DomainModel)
admin.site.register(BlackList)
admin.site.register(IPRateRule)
admin.site.register(IPConnectionModel)
admin.site.register(ScrapModel)
admin.site.register(DeviceStatisticModel)
admin.site.register(ScrapComplainModel)
