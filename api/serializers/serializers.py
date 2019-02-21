def get_error_desc(request_serializer):
    field = list(request_serializer.errors.keys())[0]
    error = list(request_serializer.errors.values())[0][0]
    return {'field': field, 'detail': error}







