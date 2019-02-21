from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    swagger_schema = None

    def post(self, request):
        login = request.POST.get('login', '')
        passwd = request.POST.get('secret', '')
        if not login or not passwd:
            return Response({'ok': False, 'detail': 'Provide login and password.'})
        else:
            user = authenticate(username=login, password=passwd)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                if created:
                    token.save()
                return Response({'ok': True, 'token': token.key})
            else:
                return Response({'ok': False, 'detail': 'Login or password incorrect'})
