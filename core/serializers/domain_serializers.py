from rest_framework import serializers
from core.models import DomainModel
from core.serializers import ConfigurationSerializer


class DomainSerializer(serializers.ModelSerializer):
    configuration = serializers.SerializerMethodField()

    class Meta:
        model = DomainModel
        fields = ('host', 'configuration')

    def get_configuration(self, obj):
        return ConfigurationSerializer(obj.configuration).data
