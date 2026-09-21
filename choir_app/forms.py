from django import forms
from .models import Member, Attendance, Contribution, Song
from django.contrib.auth.models import User

# 1. FORMU Y'INDIRIMBO
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'lyrics', 'audio_file'] # 'audio_file' nshya

# 2. FORMU Y'ABARIRIMBYI
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'voice']

# 3. FORMU Y'AMATURO N'IMISANZU
class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['member', 'purpose', 'amount']

# 4. FORMU Y'ATTENDANCE
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['member', 'status']

# 5. FORMU YO KWIYANDIKISHA (IYI NI YO YARI YABUZE IRI GUTEZA IKOSA!)
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
