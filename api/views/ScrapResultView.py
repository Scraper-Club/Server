from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import *
from api.views.ScraperApiView import ScraperApiView
from core.proxies import Scrap


class ScrapResultView(ScraperApiView):
    @swagger_auto_schema(
        operation_id='Get scrap result',
        responses={
            200: 'Returns html-page (Content-type=text/html)',
            401: 'Wrong token or no token provided',
            404: 'Such scrap doesn`t exist. (Url not scraped yet, or result have been deleted)',
        }
    )
    def get(self, request, scrap_id):
        """API call to get html content of scrap"""
        scraper = request.user.scraper
        try:
            scrap = scraper.get_scrapes().get(pk=scrap_id)
            result = scrap.get_result_str()
            return HttpResponse(result, content_type="text/html")
        except Scrap.DoesNotExist:
            return Response(data={'detail': 'Scrap doesn`t exist.'}, status=HTTP_404_NOT_FOUND)
