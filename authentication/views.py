#Standard library imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse

#Related third party imports.
from passlib.hash import django_pbkdf2_sha256 as handler


#Local application/library specific imports.
from authentication.forms import SignUpForm


# User Register View
class AuthRegisterView(View):
    form_class = SignUpForm
    template_name = 'auth/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()

        return render(request, self.template_name, {'form': form})


class AuthLoginView(View):
    pass
# User Logout View
class AuthLogoutView(View):
    def post(self, request, *args, **kwargs ):
        logout(request)
        return redirect('login')

# User Change Password View
class PasswordChangeView(View):
    def post(self, request, *args, **kwargs):
        current_password = request.POST.get('currentPassword', None)
        new_password = request.POST.get('newPassword', None)
        confirm_password = request.POST.get('confirmNewPassword', None)
        try:
            user = get_object_or_404(User, email=request.user.email)
        except:
            user=None
        if user:
            if handler.verify(current_password, user.password):
                user.set_password(confirm_password)
                user.save()
                return JsonResponse({'msg':"password Change Successfully",'success':True})
            else:
                return JsonResponse({'error':"Invalid current Password!",'success':False})
        else:
            return JsonResponse({'error':"User Does Not Exist",'success':False})

class ProfileView(View):
    pass

class AuthPasswordResetView(View):
    pass