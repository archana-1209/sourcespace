#Standard library imports.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
import random
import threading
from django.core.mail import send_mail
from django.conf import settings


#Related third party imports.
from passlib.hash import django_pbkdf2_sha256 as handler


#Local application/library specific imports.
from authentication.forms import SignUpForm
from authentication.models import OTP


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
    def get(self, request, *args, **kwargs):
        email=request.GET.get('email',None)
        if email:
            try:
                user = get_object_or_404(User,email=email)
            except:
                user=None
            if user:
                otp = random.randrange(1234, 99999, 3)
                receiver = user.get_full_name()
                subject = 'OTP from **Website Name**' + ' : ' + str(otp)
                text = 'Hi '+ receiver+' Your OTP from Learnopad.com is: ' + str(otp) + 'This OTP is valid for 7 minutes only!'
                send_mail(str(subject), text, settings.EMAIL_HOST_USER, [user.email,], fail_silently=False)
                
                # its automatically run after 7 minutes(420.0 seconds) and delete the otp object from database 
                def expire():
                    try:
                        otp_obj = get_object_or_404(OTP, sender=user.email)
                        otp_obj.delete()
                    except:
                        pass
                
                otp_obj,created = OTP.objects.get_or_create(sender=user.email)
                otp_obj.value = otp
                otp_obj.save()
                threading.Timer(420.0, expire).start()
                return JsonResponse({'success':True,"message":"Please check your email you will be received OTP "})
            else:
                return JsonResponse({'success':False ,"message":"please Sign up"})
        else:
            return JsonResponse({'success':False })
   

    def post(self, request, *args, **kwargs):
        email=request.POST.get('email',None)
        if email:
            user = User.objects.get(email=email)
            try:
                otp_obj = get_object_or_404(OTP, sender=user.email)
            except:
                return JsonResponse({'success':False ,"message":"Your OTP has been Expired"})
            
            otp =  request.POST.get('otp',None)
            new_password =  request.POST.get('new_password',None)
            confirm_password =  request.POST.get('confirm_password',None)
            if str(new_password) == str(confirm_password):

                if otp_obj.value == otp:
                    user.set_password(confirm_password)
                    user.save()
                    return JsonResponse({'success':True ,"message":"Your password is successfully recoverd"})

                else:
                    return JsonResponse({'success':False ,"message":"Invalid OTP"})
      
            else:
                return JsonResponse({'success':False ,"message":"Password Must Be Same"})
     
        else:
            return JsonResponse({'success':False})
