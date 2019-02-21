from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AndroidAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    swagger_schema = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, args, kwargs)
        self.scraper = request.user.scraper
        self.device = request.device
        self.ip = request.ip_address
