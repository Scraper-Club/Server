from rest_framework.response import Response

from ..AndroidAPIView import AndroidAPIView


class CheckDeviceRegisteredView(AndroidAPIView):
    def post(self, request):
        if request.device:
            content = {'ok': True}
        else:
            content = {'ok': False}
        return Response(content)
