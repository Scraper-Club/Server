from rest_framework import serializers

from core.serializers.scrap_serializers import ScrapSerializer
from .UrlInfoSerializer import ShortUrlInfoSerializer


class HttpBadRequestSerializer(serializers.Serializer):
    field = serializers.CharField(required=True, help_text='Field name with error')
    detail = serializers.CharField(required=True, help_text='Error detail')


class GetUrlsResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True, default=0, help_text='Number of urls in list')
    urls_list = ShortUrlInfoSerializer(many=True)


class GetScrapesResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True, default=0, help_text='Number of scrapes in list')
    scrapes_list = ScrapSerializer(many=True)

class SendScrapResponseSerializer(serializers.Serializer):
    remote_code = serializers.IntegerField()
