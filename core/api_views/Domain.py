from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from core.proxies import Domain


class DomainAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    swagger_schema = None

    def delete(self, request, domain_id):
        scraper = request.user.scraper
        try:
            domain = scraper.get_domains().get(pk=domain_id)
        except Domain.DoesNotExist:
            return Response(data={'detail': 'Domain not found'}, status=HTTP_404_NOT_FOUND)

        domain.delete()
        return Response()