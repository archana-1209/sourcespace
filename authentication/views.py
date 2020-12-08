from django.shortcuts import render
from django.views.generic import View
from authentication.forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
class register_view(View):
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

class AuthLogoutView(View):
    pass
class change_password_view(View):
    pass
class profile_view(View):
    pass
class AuthPasswordResetView(View):
    pass