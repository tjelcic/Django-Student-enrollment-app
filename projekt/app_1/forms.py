from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from . models import Korisnik, Predmeti, Upisi

class NewUserForm(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = ("email", "username", 'role', 'status', "first_name", "last_name", "password1", "password2")

class UserForm(ModelForm):
    class Meta:
        model = Korisnik
        fields = ("email", "username", 'status', "first_name", "last_name")

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required')
    class Meta:
        model = Korisnik
        fields = ("email", "username", 'status', "password1", "password2")

class PredmetForm(ModelForm):
    class Meta:
        model = Predmeti
        fields = ('name', 'kod', 'program', 'ects', 'sem_red', 'sem_izv', 'izborni', 'nositelj')

class UpisiForm(ModelForm):
    class Meta:
        model = Upisi
        fields = ('student_id', 'predmet_id', 'status') 
