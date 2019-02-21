from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

from api.serializers import ScraperSerializer
from .ScraperApiView import ScraperApiView


class ScraperUserView(ScraperApiView):
    @swagger_auto_schema(
        responses={
            200: ScraperSerializer,
            401: 'Wrong token or no token provided',
        },
        operation_id='Get scraper user info'
    )
    def get(self, request):
        """
        API method to information about current user

        """
        return Response(ScraperSerializer(request.user.scraper).data)