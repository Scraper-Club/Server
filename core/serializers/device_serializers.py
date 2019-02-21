from rest_framework import serializers
from core.models import DeviceModel, DeviceStatisticModel


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceModel
        fields = ('device_id','vendor','model','android_version')


class DeviceStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceStatisticModel
        fields = ('scrapes_count','complains_count','is_blocked')
        read_only_fields = ('scrapes_count','complains_count','is_blocked')
