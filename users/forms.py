from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class SupportGroupHelpRequest_form(ModelForm):
    class Meta:
        model = SupportGroupHelpRequest
        fields = ["about", "message", "user", "support_gourp"]


class SupportGroupJoinRequest_form(ModelForm):
    class Meta:
        model = SupportGroupJoinRequest
        fields = ["message", "user", "support_gourp"]


class Profile_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            


    class Meta:
        model = Profile
        fields = [ 'resedence', "cv", "phone_numer", "branch_of_interest", 'branch_of_interest_degree_type']


class user_procedures_form(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-select mb-3'
            


    class Meta:
        model = Profile
        fields = [ 'current_procedure']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email', 'username')

    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')

       if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")

       if User.objects.filter(username=username).exists():
            raise ValidationError("Username used")

       return self.cleaned_data
    



