from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import *
from api.views.ScraperApiView import ScraperApiView
from core.proxies import Scrap
from core.serializers import ScrapSerializer


class ScrapView(ScraperApiView):
    @swagger_auto_schema(
        operation_id='View scrap info',
        responses={
            200: ScrapSerializer,
            401: 'Wrong token or no token provided',
            404: 'Such scrap doesn`t exist. (Url not scraped yet, or result have been deleted)',
        }
    )
    def get(self, request, scrap_id):
        """
        API call to get information about scrap.
        """
        scraper = request.user.scraper
        try:
            scrap = scraper.get_scrapes().get(pk=scrap_id)
            return Response(ScrapSerializer(scrap).data)
        except Scrap.DoesNotExist:
            return Response(data={'detail': 'Scrap doesn`t exist.'}, status=HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id='Delete scrap result',
        responses={
            200: 'Scrap deleted',
            401: 'Wrong token or no token provided',
            404: 'Such scrap doesn`t exist. (Url not scraped yet, or result have been deleted)',
        }
    )
    def delete(self, request, scrap_id):
        """
        API call to delete scrap.
        """
        user = request.user.scraper
        try:
            scrap = user.get_scrapes().get(id=scrap_id)
            scrap.delete()
            return Response(data={'detail': 'Scrap deleted.'})
        except Scrap.DoesNotExist:
            return Response(data={'detail': 'Scrap doesn`t exist.'}, status=HTTP_404_NOT_FOUND)