from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from core.proxies import Device
from ..AndroidAPIView import AndroidAPIView


# TODO research bug in failure without accessing the body
class RegisterDeviceView(AndroidAPIView):
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
        return Response({'ok': True})
