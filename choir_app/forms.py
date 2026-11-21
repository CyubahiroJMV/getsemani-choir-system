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
    contact_input = forms.CharField(
        label="Email cyangwa Numero ya Telefone",
        widget=forms.TextInput(attrs={'placeholder': 'Andika email cyangwa numero ya telefone...'})
    )
    password = forms.CharField(
        label="Ijambo ry'ibanga (Password)",
        widget=forms.PasswordInput(attrs={'placeholder': 'Andika password...'})
    )
    confirm_password = forms.CharField(
        label="Emeza Ijambo ry'ibanga",
        widget=forms.PasswordInput(attrs={'placeholder': 'Subiramo password...'})
    )

   class Meta:
        model = User
        fields = ['username']

   def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Ijambo ry'ibanga (Passwords) ntirihura!")
        return cleaned_data

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








