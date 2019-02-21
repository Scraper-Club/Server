from core.proxies import Device, IPAddress


class ScraperDeviceMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            device_id = request.META['HTTP_DEVICE_ID']
            print(device_id)
            request.device = Device.objects.get(pk=device_id)
        except KeyError:
            request.device = None
            print('Device id doesnt set')
        except Device.DoesNotExist:
            request.device = None
            print('Device not registered')

        response = self.get_response(request)
        return response


class ScraperIPMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if not remote_addr:
            remote_addr = request.META.get('HTTP_X_REAL_IP', '')

        if remote_addr:
            print(f'Remote ip:{remote_addr}')
            try:
                ip = IPAddress.objects.get(ip_address=remote_addr)
            except IPAddress.DoesNotExist:
                ip = IPAddress.objects.create(ip_address=remote_addr)

            request.ip_address = ip
        else:
            print('No ip from request')
            request.ip_address = None

        response = self.get_response(request)
        return response
