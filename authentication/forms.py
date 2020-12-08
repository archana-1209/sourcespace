from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
class SignUpForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    name=forms.CharField(max_length = 200)

    class Meta:
        model = User
        fields = ("email", "password1", "password2",'name')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username=self.cleaned_data["email"]
        user.first_name=self.cleaned_data["name"].split(' ')[0]
        user.last_name=self.cleaned_data["name"].split(' ')[1]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user
    
    def clean(self):
        form_data = self.cleaned_data
        email=form_data.get("email")

        try:
            user=User.objects.get(email=email)
        except ObjectDoesNotExist:
            user=None
        if user:
            raise ValidationError("email is already exist")

        password1 = form_data.get("password1")
        password2 = form_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords did not match")
        return form_data