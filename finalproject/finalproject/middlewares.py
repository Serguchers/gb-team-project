from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse

class CheckIsUserBanned:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_banned:
                raise PermissionDenied()
            else:
                return self.get_response(request)
        else:
            return self.get_response(request)