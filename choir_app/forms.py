from django import forms
from django.contrib.auth.models import User
from .models import Member, Song, Contribution

# 1. FORM FOR MEMBERS (KUKOSORA NKURU: GUHA FORM URUHUSHYA RWO KUBIKA PHONE)
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'voice', 'phone'] # Twongeyemo 'phone' ngo ifomu iyinjize muli database


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

# 5. ADMIN REGISTER FORM (KUKOSORA KAMWE KU KAMWE: DYNAMIC DUAL CONTACT VALIDATION)
class AdminRegisterForm(forms.ModelForm):
    contact_input = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Andika email cyangwa numero ya telefone...'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Andika Password...'}))
    
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': "Izina rya User (Username)..."}),
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
