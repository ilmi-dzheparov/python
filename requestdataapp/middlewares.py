from datetime import datetime

from django.http import HttpRequest, HttpResponse


def set_useragent_on_request_middleware(get_response):
    print('Initial call')
    def middleware(request: HttpRequest):
        print("before get response")
        if 'HTTP_USER_AGENT' in request.META:
            request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        # print(request.datetime.now)
        print("after get response")
        return response
    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.datetime_last_request = {}
        self.datetime_now_request = {}

    def __call__(self, request: HttpRequest):
        if self.requests_count == 0:
            ip_address = request.META["REMOTE_ADDR"]
            request.ip_address = ip_address
            self.datetime_last_request[ip_address] = datetime.now()
            self.datetime_now_request[ip_address] = datetime.now()

            self.requests_count += 1
            request.allowed = True
            response = self.get_response(request)
            self.responses_count += 1
            print(self.requests_count, request.allowed)
            return response

        ip_address = request.META["REMOTE_ADDR"]
        request.ip_address = ip_address
        self.requests_count += 1
        print("requests count", self.requests_count)
        self.datetime_now_request[ip_address] = datetime.now()
        timeout = self.datetime_now_request[ip_address].timestamp() - self.datetime_last_request[ip_address].timestamp()
        if timeout < 1:
            request.allowed = False
        else:
            request.allowed = True
            self.datetime_last_request[ip_address] = datetime.now()
        print(timeout, request.allowed)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses count", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")

