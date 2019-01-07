from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, JsonResponse

class Filter(MiddlewareMixin):
    def process_request(self, request):
        request_type = (request.path).split("/")[1]
        user_type = request.session.get("user_type", "")
        
	if request_type == "admin":
	    pass
	elif user_type == "":
            if request_type == "user" or request_type == "" or request_type == "mobile":
                pass
            else:
                return HttpResponse(status=404)
        elif user_type == "info":
            if request_type == "info" or request_type == "user" or request_type == "":
                pass
            else:
                return HttpResponse(status=404)
        elif user_type == "student":
            if request_type == "student" or request_type == "user" or request_type == "":
                pass
            else:
                return HttpResponse(status=404)
        elif user_type == "apartment":
            if request_type == "apartment" or request_type == "user" or request_type == "":
                pass
            else:
                return HttpResponse(status=404)



    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     print("M1.process_view")
    #     response = callback(request, *callback_args, **callback_kwargs)
    #     return response
    #
    # def process_response(self, request, response):
    #     print('M1.response')
    #     return response

