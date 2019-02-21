from rest_framework.response import Response

from core.models import UrlStatus
from core.proxies import Url
from .answers import DEVICE_UNREGISTERED
from .AndroidAPIView import AndroidAPIView


class BadUrlView(AndroidAPIView):
    def post(self, request, url_id):
        if not self.device:
            return Response(DEVICE_UNREGISTERED)

        try:
            url = Url.objects.get(pk=url_id)
        except:
            return Response({'ok': False})

        if url.status == UrlStatus.SCRAPING:
            url.delete()

        return Response({'ok': True})
