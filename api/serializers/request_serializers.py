from rest_framework import serializers

from core.models import IPRate


class GetUrlsRequestSerializer(serializers.Serializer):
    pool = serializers.ChoiceField(
        default='all',
        choices=('all', 'public', 'private'),
        help_text='From which pool items to take'
    )
    limit = serializers.IntegerField(
        default=10,
        min_value=1,
        help_text='How many items display'
    )
    # status = serializers.ChoiceField(default=None, allow_null=True, choices=('scraped', 'sraping', 'not_scraped'), help_text='Select only urls with such status')


class UploadUrlRequestSerializer(serializers.Serializer):
    url = serializers.URLField(required=True, help_text='URL for scraping')
    conf_type = serializers.ChoiceField(default=None, choices=('domain', 'url'), allow_null=True)
    wait_time = serializers.IntegerField(default=3, help_text='Wait time in seconds after page was loaded', min_value=0)

    scroll_count = serializers.IntegerField(
        default=1,
        help_text='Times to scroll the page down after loading',
        min_value=0
    )
    scroll_delay = serializers.IntegerField(
        default=1,
        help_text='Wait time in seconds after each scrolling',
        min_value=0
    )
    ip_rate_type = serializers.ChoiceField(
        default=IPRate.UNLIMITED,
        choices=(IPRate.UNLIMITED, IPRate.PER_DAY, IPRate.PER_HOUR),
        help_text='IP rate for domain of this url'
    )
    ip_rate_limit = serializers.IntegerField(
        default=1000,
        min_value=0,
        help_text='Matters only if rate type is not unlimited'
    )
    pool = serializers.ChoiceField(
        default='waiting',
        choices=('private', 'public', 'waiting'),
        help_text='Pool for url'
    )


class GetScrapesRequestSerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        default=10,
        min_value=1,
        help_text='How many items to display'
    )


class SendScrapRequestSerializer(serializers.Serializer):
    destination = serializers.URLField(
        required=True,
        help_text='URL where scrap will be send by POST request'
    )


class PatchUrlRequestSerializer(serializers.Serializer):
    pool = serializers.ChoiceField(
        choices=('private', 'public', 'waiting'),
        help_text='Pool for url'
    )
