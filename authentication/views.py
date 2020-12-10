from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import logout





# Implementation of logout using CBV

class AuthLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
        
