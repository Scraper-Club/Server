from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import *

from api.serializers import GetScrapesRequestSerializer, GetScrapesResponseSerializer, HttpBadRequestSerializer, \
    get_error_desc
from api.views.ScraperApiView import ScraperApiView


class ScrapesView(ScraperApiView):

    @swagger_auto_schema(
        operation_id='View recent scrapes',
        query_serializer=GetScrapesRequestSerializer,
        responses={
            200: GetScrapesResponseSerializer,
            204: 'No scrapes yet',
            400: HttpBadRequestSerializer,
            401: 'Wrong token or no token provided',
        }
    )
    def get(self, request):
        """
        API call to get recents scrapes
        """
        scraper = request.user.scraper
        params = GetScrapesRequestSerializer(data=request.data)
        if not params.is_valid():
            return Response(HttpBadRequestSerializer(get_error_desc(params)), status=HTTP_400_BAD_REQUEST)

        limit = params.data['limit']
        scrapes = list(scraper.get_scrapes().order_by('-upload_date')[:limit])
        scrapes_count = len(scrapes)

        if scrapes_count == 0:
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(GetScrapesResponseSerializer({'count': scrapes_count, 'scrapes_list': scrapes}).data)

    @swagger_auto_schema(
        operation_id='Delete all scrapes',
        responses={
            200: 'Scrapes deleted',
            204: 'No scrapes yet',
            401: 'Wrong token or no token provided',
            404: 'Such scrap doesn`t exist. (Url not scraped yet, or result have been deleted)',
        }
    )
    def delete(self, request):
        """
        API call to delete all scrapes
        """
        scraper = request.user.scraper
        count = scraper.get_scrapes().count()
        if count == 0:
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            scraper.get_scrapes().delete()
            return Response({'detail': 'Scrapes deleted.', 'count': count})
