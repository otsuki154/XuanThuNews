from django.shortcuts import render
from .define import *
class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            # Nếu có lỗi 404, hiển thị template tùy chỉnh
            return render(request, TABLE_PATH_FILE + '404.html', status=404)
        return response