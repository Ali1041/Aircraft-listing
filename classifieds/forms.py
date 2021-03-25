from django import forms
# from registration.forms import RegistrationForm
from django_registration.forms import RegistrationForm
from . import models


class MyCustomUserForm(RegistrationForm):
    class Meta:
        model = models.User
        fields = ['email', 'password1', 'password2']


class ClassifiedForm(forms.ModelForm):
    class Meta:
        model = models.Classified
        exclude = ['user', 'date_time', 'classified_status', 'payment_completed']

        widgets = {
            "commercial_aircraft": forms.RadioSelect(attrs={"class": "list"}),
            "aircraft_type": forms.Select(attrs={"class": "form-control"}),
            "aircraft_make": forms.Select(attrs={"class": "form-control"}),
            "serial_number": forms.TextInput(attrs={"class": "form-control"}),
            "year_of_make": forms.Select(attrs={"class": "form-control"}),
            "aircraft_status": forms.RadioSelect(attrs={"class": "list"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "6"}),
            "engine_details": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            "interior": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            "exterior": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            "avionics": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            "maintenance_status": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            "additional_information": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
        }


class ClassifiedImageForm(forms.ModelForm):
    class Meta:
        model = models.ClassifiedImage
        exclude = ['classified']


# class SearchForm(forms.ModelForm):
#     min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "ex: $10000"}))
#     max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "ex: $50000"}))
#
#     min_year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "ex: 1980"}))
#     max_year = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "ex: 2018"}))
#
#     class Meta:
#         model = models.Classified
#         fields = ['aircraft_type', 'aircraft_make']
#
#         widgets = {
#             "aircraft_type": forms.CheckboxSelectMultiple(),
#             "aircraft_make": forms.CheckboxSelectMultiple(),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(SearchForm, self).__init__(*args, **kwargs)
#         self.fields['aircraft_type'].empty_label = None
#         self.fields['aircraft_make'].empty_label = None


# class ContactSellerForm(forms.Form):
#     name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control"}))
#     email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control"}))
#     message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}))
#

class ContactForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name.."}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your email.."}))
    subject = forms.CharField(max_length=255, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject.."}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "rows": "8", "placeholder": "Message.."}))
