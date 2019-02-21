from rest_framework import serializers

from core.models import Scraper


class ScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scraper
        fields = ('id', 'tokens', 'scrapes', 'complains')
        read_only_fields = ('__all__',)