def read_header(request):
    return request.headers.get('X-Request-Id')
