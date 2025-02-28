from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, MotherTongue

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    mother_tongue = forms.ModelChoiceField(queryset=MotherTongue.objects.all(), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.mother_tongue = self.cleaned_data['mother_tongue']
            user.profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mother_tongue']
    