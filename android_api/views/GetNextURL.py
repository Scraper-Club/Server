from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .answers import *
from core.proxies import Url
from .AndroidAPIView import AndroidAPIView
import random


def random_last(self, device, ip_address):
    rint = random.randint(0, 10)
    queryset = Url.public_pool.available_for_scraping(device, ip_address)
    if rint > 5:
        return queryset.order_by('-owner__scraper__last_scrap')
    else:
        return queryset.order_by('?')


class GetNextURL(AndroidAPIView):
    url_sort_mechanism = random_last

    def get(self, request):
        if not self.device:
            return Response(DEVICE_UNREGISTERED)

        if self.ip.is_over_limit():
            return Response(IP_LIMIT)

        pool = request.GET.get('pool', 'public')

        if pool == 'public':
            return self.get_next_public_url(request)
        elif pool == 'private' and self.scraper.allow_private:
            return self.get_private_url(request)
        else:
            return Response({'detail': 'Wrong pool.'}, status=HTTP_400_BAD_REQUEST)

    def get_private_url(self, request):
        queryset = self.scraper.get_private_urls().available_for_scraping(device=self.device, ip_address=self.ip)
        if queryset.exists():
            return self.start_scrap_url(queryset[0], request)
        else:
            return Response(NO_AVAILABLE_URLS)

    def get_next_public_url(self, request):
        response = None
        queryset = self.url_sort_mechanism(device=self.device, ip_address=self.ip)

        if queryset.exists():
            response = self.start_scrap_url(queryset[0], request)
        else:
            queryset = Url.waiting_pool.available_for_scraping(device=self.device, ip_address=self.ip) \
                .filter(owner__scraper__tokens__gt=0).order_by('?')
            if queryset.exists():
                response = self.start_scrap_url(queryset[0], request)

        if not response:
            return Response(NO_AVAILABLE_URLS)
        else:
            return response

    def start_scrap_url(self, url, request):
        if url.owner != request.user:
            url.owner.scraper.revoke_token()
        url.on_scrap_started()
        configuration = url.get_configuration()
        config = {
            'wait_time': configuration.wait_time,
            'scroll_count': configuration.scroll_count,
            'scroll_delay': configuration.scroll_delay,
        }
        return Response({'ok': True, 'id': url.id, 'url': str(url), 'config': config})