from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Member, Song, Contribution, Attendance
from .forms import MemberForm, AttendanceForm, ContributionForm, SongForm, UserRegisterForm

# 1. HOME PAGE
def index(request):
    songs = Song.objects.all()
    context = {'songs': songs}
    return render(request, 'choir_app/index.html', context)

# 2. DASHBOARD PANEL Y'ABAYOBOZI (ADMIN ONLY)
@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_staff: 
        return redirect('songs_list')
        
    members = Member.objects.all()
    songs = Song.objects.all()
    member_form = MemberForm(request.POST or None)
    attendance_form = AttendanceForm(request.POST or None)
    contribution_form = ContributionForm(request.POST or None)
    
    if request.method == 'POST' and 'add_song' in request.POST:
        song_form = SongForm(request.POST, request.FILES)
        if song_form.is_valid():
            song_form.save()
            return redirect('dashboard')
    else:
        song_form = SongForm()
    
    if request.method == 'POST':
        if 'add_member' in request.POST and member_form.is_valid():
            member_form.save()
            return redirect('dashboard')
        elif 'add_contribution' in request.POST and contribution_form.is_valid():
            contribution_form.save()
            return redirect('dashboard')

    context = {
        'members': members,
        'songs': songs,
        'member_form': member_form,
        'attendance_form': attendance_form,
        'contribution_form': contribution_form,
        'song_form': song_form,
    }
    return render(request, 'choir_app/dashboard_new.html', context)

# 3. PAJI YO KWINJIRA (LOGIN)
def admin_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        selected_role = request.POST.get('user_role') 
        if form.is_valid():
            user = form.get_user()
            if selected_role == 'admin':
                if user.is_staff:
                    auth_login(request, user)
                    return redirect('dashboard')
                else:
                    messages.error(request, "Iyi konti ntabwo ifite uburenganzira bwa Admin Portal!")
            elif selected_role == 'singer':
                auth_login(request, user)
                return redirect('songs_list')
        else:
            messages.error(request, "Username cyangwa Password ntabwo ari zo!")
    return render(request, 'choir_app/login.html', {'form': form})

# 4. PAJI Y'IMISANZU N'AMATURO
@login_required(login_url='login')
def contributions_list(request):
    selected_purpose = request.GET.get('purpose', 'all')
    totals_by_purpose = Contribution.objects.values('purpose').annotate(total_pieces=Sum('amount')).order_by('purpose')
    
    if selected_purpose == 'all' or not selected_purpose:
        contributions = Contribution.objects.all()
        total_data = contributions.aggregate(Sum('amount'))
        current_total = total_data['amount__sum'] or 0
    else:
        contributions = Contribution.objects.filter(purpose=selected_purpose)
        total_data = contributions.aggregate(Sum('amount'))
        current_total = total_data['amount__sum'] or 0

    context = {
        'contributions': contributions,
        'totals_by_purpose': totals_by_purpose,
        'selected_purpose': selected_purpose,
        'current_total': current_total,
    }
    return render(request, 'choir_app/contributions.html', context)

# 5. URUTONDE RW'ABARIRIMBYI (HANO TWONGEREYEHO UBURENGANZIRA BW'UWINJIYE)
@login_required(login_url='login')
def members_list(request):
    members = Member.objects.all()
    # Guhereza paji amakuru y'uwinjiye live
    return render(request, 'choir_app/members.html', {'members': members})

# 6. URUTONDE RW'INDIRIMBO ZOSE
@login_required(login_url='login')
def songs_list(request):
    search_query = request.GET.get('q', '')
    if search_query:
        songs = Song.objects.filter(
            Q(title__icontains=search_query) | Q(lyrics__icontains=search_query)
        )
    else:
        songs = Song.objects.all()
    return render(request, 'choir_app/songs.html', {'songs': songs})

# 7. REGISTRATION N'IZINDI FUNCTIONS
def admin_register(request):
    form = UserRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return redirect('login')
    return render(request, 'choir_app/register.html', {'form': form})

def admin_logout(request):
    auth_logout(request)
    return redirect('index')

def member_portal(request):
    return redirect('songs_list')

def member_profile(request):
    return render(request, 'choir_app/profile.html')
