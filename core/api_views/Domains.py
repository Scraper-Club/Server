from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DomainsAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    swagger_schema = None

    def delete(self, request):
        scraper = request.user.scraper
        scraper.get_domains().delete()
        return Response()