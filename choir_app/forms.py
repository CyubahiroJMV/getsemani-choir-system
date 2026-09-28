from django import forms
from django.contrib.auth.models import User
from .models import Member, Song, Contribution

# 1. FORM FOR MEMBERS
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'voice']

# 2. FORM FOR SONGS
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'audio_file', 'lyrics']

# 3. FORM FOR CONTRIBUTIONS
class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['member', 'purpose', 'amount']

# 4. FIX IMPORT ERROR: ATTENDANCE FORM (YASHIZWEMO NGO VIEW IKORE NEZA)
class AttendanceForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# 5. ADMIN REGISTER FORM 
class AdminRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Andika Password...'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Izina rya Telefone cyangwa Izina ryawe..."}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# 6. ADMIN LOGIN FORM
class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Andika Username...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Andika Password...'}))
