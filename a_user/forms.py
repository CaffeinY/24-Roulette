from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password!")
        return cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_confirm_password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm = cleaned_data['confirm']
        if password and confirm and password != confirm:
            raise forms.ValidationError('Passwords did not match!')
        return cleaned_data
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('bio', 'image')
#         widgets = {
#             'bio': forms.Textarea(attrs={'id': 'id_bio_input_text',
#                                          'class': 'form-control',
#                                          'rows': 3,
#                                          'style': 'width: 500px; margin-bottom: 10px;'}),
                                    
#             'image': forms.FileInput(attrs={'id': 'id_profile_picture'})
#         }
#     def clean_image(self):
#         image = self.cleaned_data['image']
#         if not image:
#             raise forms.ValidationError('You must upload a profile image')
#         return image