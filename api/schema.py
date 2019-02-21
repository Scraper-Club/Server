import json
from urllib.parse import urlencode

from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token

from drf_yasg.inspectors import ViewInspector, SwaggerAutoSchema


class XcodeAutoSchema(SwaggerAutoSchema):
    def __init__(self, view, path, method, components, request, overrides):
        super(XcodeAutoSchema, self).__init__(view, path, method, components, request, overrides)

    def get_operation(self, operation_keys):
        operation = super(XcodeAutoSchema, self).get_operation(operation_keys)
        if not self.request._request.user.is_anonymous:
            try:
                token = Token.objects.get(user=self.request._request.user)
            except Token.DoesNotExist:
                token = None
        else:
            token = None
        try:
            security = operation.security
            headers = {}
        except:
            if token:
                headers = {
                    'Authorization': f'Token {token}'
                }
            else:
                headers = {
                    'Authorization': 'Token ecb4cf2fb63bcc368deeaeb9872c9caecff988e9'
                }
        payload, query = self.build_payload(operation)
        template_context = {
            "headers": headers,
            "request_url": self.request._request.build_absolute_uri(self.path),
            "method": self.method,
            "payload": payload,
            "query": query,
            "query_format": urlencode(query, safe='/@')
        }

        if 'upload url' in operation.operation_id.lower():
            serializer = self.get_request_serializer()
            serializer.__init__(data = {'url':'http://example.com'})
            if serializer.is_valid():
                json.dumps(serializer.data)
            template_context['payload'] = json.dumps(serializer.data, indent=2)
            template_context['headers']['Content-Type']='application/json'
            curl_sample = {
                "lang": "curl",
                "source": render_to_string('curl_json.html', template_context).strip("\\")
            }
        else:
            curl_sample = {
                "lang": "curl",
                "source": render_to_string('curl_sample.html', template_context).strip("\\")
            }

        operation.update({
            'x-code-samples': [
                curl_sample,
                {
                    "lang": "python",
                    "source": render_to_string('python_sample.html', template_context)
                }
            ]
        })
        return operation

    def build_payload(self, operation):
        values = {
            'url': 'http://example.com',
            'value': 'http://example.com',
            'destination': 'http://example.com',
            'pool':'waiting',
        }
        payload = {}
        query = {}
        for param in operation.parameters:
            if param.get('in') == 'body':
                # make it a payload
                schema = param.schema.resolve(self.components)
                required = schema.required
                for prop, sch in schema.properties.items():
                    if prop in required:
                        payload[prop] = values[prop]
            if param.get('in') == 'query':
                if param.required:
                    query[param.name] = values[param.name]
        return payload, query
