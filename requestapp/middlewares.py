from django.http import HttpRequest
from timeit import default_timer

from django.shortcuts import render


def set_useragent_on_request_middleware(get_responce):

    # print("initial call")

    def middleware(request: HttpRequest):
        # print("before get responce")
        # request.user_agent = request.META["HTTP_USER_AGENT"]
        responce = get_responce(request)
        # print("after get responce")
        return responce

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_responce):
        self.get_responce = get_responce
        self.requests_count = 0
        self.responses_count = 0
        self.exception_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        # print("requests_count", self.requests_count)
        responce = self.get_responce(request)
        self.responses_count += 1
        # print("responses_count", self.responses_count)
        return responce

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print("got", self.exception_count, "exceptions so far")


class ThrottlingMiddleware:
    def __init__(self, get_responce):
        self.get_responce = get_responce
        self.start_time = 0
        self.ip_address = ''

    def __call__(self, request: HttpRequest):
        times_delay = 0.01
        if request.META["REMOTE_ADDR"] == self.ip_address and (default_timer() - self.start_time) < times_delay:
            context = {
                'result': request.META["REMOTE_ADDR"],
            }
            return render(request, 'requestapp/error.html', context=context)
        self.ip_address = request.META["REMOTE_ADDR"]
        self.start_time = default_timer()
        responce = self.get_responce(request)

        return responce