from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms
from django.core.exceptions import ValidationError

class UniversityForm(ModelForm):
    class Meta:
        model = University
        fields = ["name", "city", "website", "programmes_page"]


class ScholarshipForm(ModelForm):
    class Meta:
        model = Scholarship
        fields = ["name", "university", "about", "support_contacts"]



class ScholarshipSessionForm(ModelForm):
    class Meta:
        model = ScholarshipSession
        fields = ["scholarship", "session", "apply_link"]
