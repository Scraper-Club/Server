from rest_framework import serializers
from core.models import ConfigurationModel
from core.proxies import Url, Scrap

WAIT_TIME_HELP_TEXT = 'Wait time in seconds after page was loaded'
SCROLL_COUNT_HELP_TEXT = 'Times to scroll the page down after loading'
SCROLL_DELAY_HELP_TEXT = 'Wait time in seconds after each scrolling'


class ConfigurationSerializer(serializers.ModelSerializer):
    wait_time = serializers.IntegerField(default=3, help_text=WAIT_TIME_HELP_TEXT, min_value=0)
    scroll_count = serializers.IntegerField(default=1, help_text=SCROLL_COUNT_HELP_TEXT, min_value=0)
    scroll_delay = serializers.IntegerField(default=1, help_text=SCROLL_DELAY_HELP_TEXT, min_value=0)

    class Meta:
        model = ConfigurationModel
        fields = ('wait_time', 'scroll_count', 'scroll_delay')


SCRAP_HELP_TEXT = 'Scrap ID if URL was scraped, otherwise null'


class UrlInfoSerializer(serializers.ModelSerializer):
    pool = serializers.CharField(source='get_pool_display', required=False)

    class Meta:
        model = Url
        fields = ('id', 'url', 'pool')
        read_only_fields = ('id', 'url', 'pool')


class ShortUrlInfoSerializer(UrlInfoSerializer):
    status = serializers.CharField(source='get_status_display', required=False)
    scrap = serializers.IntegerField(source='get_scrap_id', required=False, allow_null=True, help_text=SCRAP_HELP_TEXT)

    class Meta:
        model = Url
        fields = ('id', 'url', 'pool', 'scrap', 'status')
        read_only_fields = ('id', 'scrap', 'status')


class FullUrlInfoSerializer(ShortUrlInfoSerializer):
    configuration = ConfigurationSerializer(source='get_configuration', required=False)

    class Meta:
        model = Url
        fields = ('id', 'url', 'pool', 'scrap', 'status', 'configuration')
        read_only_fields = ('id', 'scrap', 'status')
