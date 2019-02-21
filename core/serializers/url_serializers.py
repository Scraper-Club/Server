from rest_framework import serializers
from core.models import UrlModel, UrlPool, ConfigurationModel


class UrlSerializer(serializers.ModelSerializer):
    pool = serializers.CharField(source='get_pool_display')

    class Meta:
        model = UrlModel
        fields = ('id', 'url', 'pool')
        read_only_fields = ('id',)


class UrlInfoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', required=False)
    configuration = serializers.SerializerMethodField()

    class Meta:
        model = UrlModel
        fields = ('id', 'url', 'status', 'pool', 'configuration')
        read_only_fields = ('id', 'status', 'configuration')

    def get_config(self, obj):
        if obj.configuration:
            configuration = obj.configuration
        else:
            configuration = obj.domain.configuration
        return ConfigurationSerializer(configuration).data


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