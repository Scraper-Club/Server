from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST

from datetime import datetime

from core.models import UrlStatus
from core.proxies import Device, Url, Scrap

from .answers import *


def get_device_request_info(request):
    user = request.user.scraper
    ip = request.ip_address
    device = request.device

    return user, device, ip


class AndroidApiView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    swagger_schema = None


class UploadUrlView(AndroidApiView):
    def post(self, request, url_id, format=None):
        user, device, ip = get_device_request_info(request)

        if not device:
            return Response(DEVICE_UNREGISTERED)

        try:
            url = Url.objects.get(id=url_id)

            if url.status != UrlStatus.SCRAPED:
                scrap = Scrap.objects.create(
                    file=request.body,
                    owner=url.owner,
                    url=url,
                    url_value=url.url,
                    scraper_user=request.user,
                    scraper_device=device,
                    ip_address=ip
                )

                url.owner.scraper.last_scrap = datetime.now()
                url.owner.scraper.save()

                url.status = UrlStatus.SCRAPED
                url.save()

                ip.on_domain_connected(domain=url.domain)
                device.used_ip_addresses.add(ip)
                user.add_scrap(url)
                device.add_scrap()
                return Response(data={'ok': True, 'detail': 'Scrap uploaded.'})
            else:
                return Response(data=URL_SCRAPED)

        except Url.DoesNotExist:
            return Response({'ok': False, 'detail': 'No such url.'})


class Login(APIView):
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


# TODO research bug in failure without accessing the body
class Register(AndroidApiView):
    def post(self, request):
        android_id = request.META.get('HTTP_DEVICE_ID', '')
        print(request.body)
        if not android_id:
            return Response({'detail', 'Device-Id header not set'}, status=HTTP_400_BAD_REQUEST)

        if request.device:
            device = Device.objects.get(pk=android_id)
            device.current_owner = request.user
            device.save()
        else:
            Device.objects.create(
                current_owner=request.user,
                device_id=android_id,
                vendor=request.POST.get('manufacturer', 'device_not_provided'),
                model=request.POST.get('model', 'device_not_provided'),
                android_version=request.POST.get('android_version', 'device_not_provided'),
            )

        content = {
            'ok': True,
        }
        return Response(content)


class Check(AndroidApiView):
    def post(self, request):
        if request.device:
            content = {'ok': True}
        else:
            content = {'ok': False}
        return Response(content)


class Stats(AndroidApiView):
    def post(self, request):
        android_id = request.META.get('HTTP_DEVICE_ID', '')
        if not android_id:
            return Response({'detail', 'Device-Id header not set'}, status=HTTP_400_BAD_REQUEST)

        if not request.device:
            return Response(DEVICE_UNREGISTERED)

        stats = request.device.get_stats(request.ip_address)
        stats['allow_private'] = request.user.scraper.allow_private
        stats['private_pool'] = request.user.scraper.get_private_urls() \
            .available_for_scraping(device=request.device, ip_address=request.ip_address).count()

        content = {
            'ok': True,
            'stats': stats,
        }
        return Response(content)
