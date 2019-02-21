from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from api.serializers import serializers
from core.models import IPRate
from core.proxies import IPAddress


class IPRateSerializer(serializers.Serializer):
    rate_type = serializers.ChoiceField(
        choices=(IPRate.UNLIMITED, IPRate.PER_HOUR, IPRate.PER_DAY),
        required=True
    )
    rate_limit = serializers.IntegerField(min_value=1, required=True)


class IPAddressAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    swagger_schema = None

    def patch(self, request, pk):
        params = IPRateSerializer(data=request.data)

        if not params.is_valid():
            field = list(params.errors.keys())[0]
            error = list(params.errors.values())[0][0]
            return Response({'field': field, 'detail': error}, HTTP_400_BAD_REQUEST)

        try:
            ip_address = IPAddress.objects.get(pk=pk)

        except IPAddress.DoesNotExist:
            return Response(data={'detail': 'IP Address not found'}, status=HTTP_404_NOT_FOUND)
        else:
            ip_address.rate_type = params.data['rate_type']
            ip_address.rate_limit = params.data['rate_limit']
            ip_address.save()

            return Response(
                {'ip': str(ip_address), 'rate_type': ip_address.rate_type, 'rate_limit': ip_address.rate_limit})

    def delete(self, request, pk):
        try:
            print('Deleting', pk)
            ip_address = IPAddress.objects.get(pk=pk)

        except IPAddress.DoesNotExist:
            return Response(data={'detail': 'IP Address not found'}, status=HTTP_404_NOT_FOUND)
        else:
            ip_address.delete()
            return Response()
