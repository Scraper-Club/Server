from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

class CheckApiKey(APIView):
    swagger_schema = None

    def post(self, request):
        api_key = request.POST.get('api_key', '')
        if api_key:
            if Token.objects.filter(key=api_key).exists():
                return Response({'ok': True})
            else:
                return Response({'ok': False, 'detail': 'Wrong api key'})
        else:
            return Response({'ok': False, 'detail': 'Api key not provided'})
