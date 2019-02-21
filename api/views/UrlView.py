from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import *

from api.serializers import FullUrlInfoSerializer, HttpBadRequestSerializer, PatchUrlRequestSerializer, get_error_desc, \
    UrlInfoSerializer
from core.models import UrlPool, UrlStatus
from core.proxies import Url
from .ScraperApiView import ScraperApiView


class UrlView(ScraperApiView):
    @swagger_auto_schema(
        responses={
            200: FullUrlInfoSerializer,
            401: 'Wrong token or no token provided',
            404: 'URL doesn`t exist'
        },
        operation_id='Get URL information'
    )
    def get(self, request, url_id):
        """
        API call to get the full information about URL.
        """

        scraper = request.user.scraper
        try:
            url = scraper.get_urls().get(pk=url_id)
        except Url.DoesNotExist:
            return Response({'detail': 'URL with such id doesn\'t exist. Maybe it was deleted.'},
                            status=HTTP_404_NOT_FOUND)

        return Response(FullUrlInfoSerializer(url).data)

    @swagger_auto_schema(
        responses={
            200: 'Deleted',
            401: 'Wrong token or no token provided',
            404: 'URL doesn`t exist'
        },
        operation_id='Delete URL'
    )
    def delete(self, request, url_id):
        """
        API call for deleting the URL. If URL is in public pool, and haven't been scraped, you'll get back your token
        """
        scraper = request.user.scraper
        try:
            url = scraper.get_urls().get(pk=url_id)
        except Url.DoesNotExist:
            return Response({'detail': 'URL with such id doesn\'t exist. Maybe it was deleted.'},
                            status=HTTP_404_NOT_FOUND)

        if url.pool == UrlPool.PUBLIC and url.status != UrlStatus.SCRAPED:
            scraper.add_token()
        url.delete()

        return Response({'detail': 'URL deleted.'})

    @swagger_auto_schema(
        request_body=PatchUrlRequestSerializer,
        responses={
            200: UrlInfoSerializer,
            400: HttpBadRequestSerializer,
            401: 'Wrong token or no token provided',
            403: 'Forbidden to move URL',
            404: 'URL doesn`t exist'
        },
        operation_id='Update URL pool'
    )
    def patch(self, request, url_id):
        """
        API call to update URL pool.
        """
        params = PatchUrlRequestSerializer(data=request.data)
        if not params.is_valid():
            return Response(HttpBadRequestSerializer(get_error_desc(params)).data, status=HTTP_400_BAD_REQUEST)
        scraper = request.user.scraper
        try:
            url = scraper.get_urls().get(pk=url_id)
        except Url.DoesNotExist:
            return Response({'detail': 'URL with such id doesn\'t exist. Maybe it was deleted.'},
                            status=HTTP_404_NOT_FOUND)

        moved = False
        add_token = False
        print(params.data['pool'])
        if params.data['pool'] == 'public' and scraper.tokens > 0:
            moved = url.move_to_public()
            if moved:
                scraper.revoke_token()

        elif params.data['pool'] == 'private':
            if url.pool == UrlPool.PUBLIC:
                add_token = True

            moved = url.move_to_private()

        elif params.data['pool'] == 'waiting':
            if url.pool == UrlPool.PUBLIC:
                add_token = True

            moved = url.move_to_waiting()

        print(moved)
        if moved:
            if add_token:
                scraper.add_token()

            return Response(UrlInfoSerializer(url).data)
        else:
            return Response({'detail': 'Update forbidden'}, status=HTTP_403_FORBIDDEN)
