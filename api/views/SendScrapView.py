import httplib2
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.status import *

from api.serializers import SendScrapResponseSerializer, HttpBadRequestSerializer, SendScrapRequestSerializer, \
    get_error_desc
from api.views.ScraperApiView import ScraperApiView
from core.proxies import Scrap

http_client = httplib2.Http()


def send_scrap(scrap, url):
    body = scrap.get_result_str()
    resp = http_client.request(
        url,
        method="POST",
        headers={'Content-type': 'text/html'},
        body=body.encode('utf-8'))[0]

    return resp.status;


class SendScrapView(ScraperApiView):
    @swagger_auto_schema(
        operation_id='Send scrap result to server',
        request_body=SendScrapRequestSerializer,
        responses={
            200: SendScrapResponseSerializer,
            400: HttpBadRequestSerializer,
            401: 'Wrong token or no token provided',
            404: 'Such scrap doesn`t exist. (Url not scraped yet, or result have been deleted)',
        },
    )
    def post(self, request, scrap_id):
        scraper = request.user.scraper
        params = SendScrapRequestSerializer(data=request.data)
        if not params.is_valid():
            return Response(HttpBadRequestSerializer(get_error_desc(params)).data, status=HTTP_400_BAD_REQUEST)

        try:
            scrap = scraper.get_scrapes().get(pk=scrap_id)
            code = send_scrap(scrap, params.data['destination'])
            return Response(SendScrapResponseSerializer({'remote_code': code}).data)
        except Scrap.DoesNotExist:
            return Response(data={'detail': 'Scrap doesn`t exist.'}, status=HTTP_404_NOT_FOUND)


# class SendMultiple(ScraperApiView):
#     @swagger_auto_schema(
#         operation_id='Send scrapes results to server',
#         responses={
#             200: 'Scrapes sent',
#             204: 'No scrapes',
#             401: 'Wrong token or no token provided',
#             404: 'Such scrap doesn`t exist. (Url not scraped yet, or result have been deleted)',
#         }
#     )
#     def post(self, request):
#         user = request.user.scraper
#         scrap_query = user.get_scrapes()
#         target_url = request.POST.get('target_url', '')
#
#         if not target_url:
#             return Response({'detail': 'No url specified.'}, status=HTTP_400_BAD_REQUEST)
#
#         if scrap_query.exists():
#             results = []
#             for scrap in scrap_query:
#                 code = send_scrap(scrap, target_url)
#                 results.append({'id': scrap.id, 'response_code': code})
#             return Response({'count': len(results), 'codes': results})
#         else:
#             return Response({'count': 0, 'detail': 'No scrapes yet.'}, status=HTTP_204_NO_CONTENT)
#





