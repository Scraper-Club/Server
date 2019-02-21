from rest_framework import serializers
from core.models import ScrapModel, ScrapComplainModel


class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapModel
        fields = (
            'id', 'url', 'url_value', 'scraper_user', 'scraper_device', 'ip_address', 'upload_date', 'complained'
        )


class ScrapComplainSerializer(serializers.ModelSerializer):
    message = serializers.CharField(max_length=300, default='Bad scrap result')

    class Meta:
        model = ScrapComplainModel
        fields = (
            'id', 'scrap', 'message', 'from_user', 'on_user', 'on_device', 'on_ip_address', 'time'
        )
