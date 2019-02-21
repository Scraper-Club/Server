from rest_framework.response import Response
from datetime import datetime

from core.models import UrlStatus
from core.proxies import Url, Scrap
from .AndroidAPIView import AndroidAPIView
from .answers import DEVICE_UNREGISTERED, URL_SCRAPED


class UploadUrlView(AndroidAPIView):
    def post(self, request, url_id, format=None):
        if not self.device:
            return Response(DEVICE_UNREGISTERED)

        try:
            url = Url.objects.get(id=url_id)

        except Url.DoesNotExist:
            return Response({'ok': False, 'detail': 'No such url.'})

        else:
            if url.status != UrlStatus.SCRAPED:
                scrap = Scrap.objects.create(
                    file=request.body,
                    owner=url.owner,
                    url=url,
                    url_value=url.url,
                    scraper_user=request.user,
                    scraper_device=self.device,
                    ip_address=self.ip
                )

                url.owner.scraper.last_scrap = datetime.now()
                url.owner.scraper.save()

                url.status = UrlStatus.SCRAPED
                url.save()

                ip.on_domain_connected(domain=url.domain)
                self.device.used_ip_addresses.add(self.ip)
                self.scraper.add_scrap(url)
                self.device.add_scrap()
                return Response(data={'ok': True, 'detail': 'Scrap uploaded.'})
            else:
                return Response(data=URL_SCRAPED)
