from urllib.parse import urlsplit

from rest_framework.response import Response
from rest_framework.status import *

from api.views.ScraperApiView import ScraperApiView
from drf_yasg.utils import swagger_auto_schema
from api.serializers import *
from core.proxies import Url, Domain
from core.serializers import ConfigurationSerializer


class UrlsView(ScraperApiView):
    @swagger_auto_schema(
        request_body=UploadUrlRequestSerializer,
        responses={
            201: UrlInfoSerializer,
            400: HttpBadRequestSerializer,
            401: 'Wrong token or no token provided',
            403: 'Adding urls is forbidden'
        },
        operation_id='Upload URL'
    )
    def post(self, request):
        """
        API method to upload url for scraping

        """
        params = UploadUrlRequestSerializer(data=request.data)
        if not params.is_valid():
            return Response(HttpBadRequestSerializer(get_error_desc(params)).data, status=HTTP_400_BAD_REQUEST)

        pool = params.data['pool']
        if pool == 'public' and request.user.scraper.tokens == 0:
            return Response({'detail': 'No tokens'}, status=HTTP_403_FORBIDDEN)
        if pool == 'private' and not request.user.scraper.allow_private:
            return Response({'detail': 'Private pool is disallowed'}, status=HTTP_403_FORBIDDEN)

        url_value = params.data['url']
        domain, created = Domain.objects.get_or_create(
            hostname="{0.netloc}".format(urlsplit(url_value)),
            owner=request.user
        )
        url = Url.objects.create(owner=request.user, url=url_value, domain=domain)
        if pool == 'public':
            url.move_to_public(save=False)
            request.user.scraper.revoke_token()

        conf_type = params.data['conf_type']

        if conf_type:
            configuration = ConfigurationSerializer(data=request.data)

            if not configuration.is_valid():
                return Response(HttpBadRequestSerializer(get_error_desc(configuration)), status=HTTP_400_BAD_REQUEST)

            conf = configuration.save(user=request.user)
            if conf_type == 'domain':
                domain.configuration = conf
                domain.save()
            elif conf_type == 'url':
                url.configuration = conf

        ip_rate_rule = url.domain.get_ip_rate_rule()
        ip_rate_rule.rate_type = params.data['ip_rate_type']
        ip_rate_rule.rate_limit = params.data['ip_rate_limit']
        ip_rate_rule.save()

        url.save()
        return Response(UrlInfoSerializer(url).data, status=HTTP_201_CREATED)

    @swagger_auto_schema(
        query_serializer=GetUrlsRequestSerializer,
        responses={
            200: GetUrlsResponseSerializer,
            204: 'No URLs matching query',
            400: HttpBadRequestSerializer,
            401: 'Wrong token or no token provided',
        },
        operation_id='Get all URLs'
    )
    def get(self, request):
        scraper = request.user.scraper
        params = GetUrlsRequestSerializer(data=request.data)
        if not params.is_valid():
            return Response(HttpBadRequestSerializer(get_error_desc(params)), status=HTTP_400_BAD_REQUEST)

        limit = params.data['limit']
        pool = params.data['pool']

        if pool == 'private':
            query_set = scraper.get_private_urls()[:limit]
        elif pool == 'public':
            query_set = scraper.get_public_urls()[:limit]
        elif pool == 'waiting':
            query_set = scraper.get_waiting_urls()[:limit]
        else:
            query_set = scraper.get_urls()[:limit]

        urls_list = list(query_set)
        count = len(urls_list)
        if count == 0:
            return Response(status=HTTP_204_NO_CONTENT)
        else:
            return Response(GetUrlsResponseSerializer({'count': count, 'urls_list': urls_list}).data)

    @swagger_auto_schema(
            responses={
                200: 'Urls deleted',
                401: 'Wrong token or no token provided',
            },
            operation_id='Delete all URLs'
        )
    def delete(self, request):
        scraper = request.user.scraper
        scraper.get_domains().delete()
        scraper.get_urls().delete()
        return Response()
