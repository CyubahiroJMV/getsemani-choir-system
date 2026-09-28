from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Member, Song, Contribution
from .forms import MemberForm, SongForm, ContributionForm, AttendanceForm, AdminRegisterForm, AdminLoginForm

# 1. HOME PAGE
def index(request):
    songs = Song.objects.all()
    return render(request, 'choir_app/index.html', {'songs': songs})

# 2. MASTER DASHBOARD PANEL Y'ABAYOBOZI (KUKOSORA: ABSOLUTE ADMIN ACCURACY LOCK)
@login_required(login_url='/login/')
def dashboard(request):
    # KUKOSORA: Gukumira umuser wese usanzwe ku nguvu z'amategeko (Izina rya admin_getsemani ryo ryahembwa rishobora kwinjira)
    if request.user.username != 'admin_getsemani' and not request.user.is_superuser:
        logout(request) # Guhita asohorwa muli system mfuruka y'imbere (Strict Terminate)
        messages.error(request, "Ntabwo mufite uburenganzira bw'Ubuyobozi bwo kureba iyi Panel!")
        return redirect('login')
        
    members = Member.objects.all()
    songs = Song.objects.all()
    contributions = Contribution.objects.all()
    
    member_form = MemberForm(request.POST or None)
    contribution_form = ContributionForm(request.POST or None)
    
    if request.method == 'POST' and 'add_song' in request.POST:
        song_form = SongForm(request.POST, request.FILES)
        if song_form.is_valid():
            song_form.save()
            messages.success(request, "Indirimbo nshya yamaze kwinjira muli Repertoire!")
            return redirect('/panel/')
    else:
        song_form = SongForm()
    
    if request.method == 'POST':
        if 'add_member' in request.POST and member_form.is_valid():
            member_form.save()
            messages.success(request, "Umuririmbyi mushya yanditswe neza usesuye!")
            return redirect('/panel/')
        elif 'add_contribution' in request.POST and contribution_form.is_valid():
            contribution_form.save()
            messages.success(request, "Umusanzu mushya winjijwe neza usesuye!")
            return redirect('/panel/')

    context = {
        'members': members,
        'songs': songs,
        'contributions': contributions,
        'member_form': member_form,
        'contribution_form': contribution_form,
        'song_form': song_form,
    }
    return render(request, 'choir_app/dashboard_new.html', context)

# 3. LIST VIEWS FOR USERS
@login_required(login_url='/login/')
def members_list(request):
    members = Member.objects.all()
    return render(request, 'choir_app/members.html', {'members': members})

# 3. LIST VIEWS FOR USERS (KUKOSORA: MASTER SEARCH ENGINE ENGINE Y'UBWIZA)
@login_required(login_url='/login/')
def songs_list(request):
    songs = Song.objects.all()
    
    # KUKOSORA: Kwakira live amakuru yanditswe muli akazu ka Search (q parameter)
    query = request.GET.get('q')
    
    if query:
        # Ibi bishakisha niba ririya jambo riri muli Title cyangwa muli Lyrics (icya rimwe)
        songs = songs.filter(title__icontains=query) | songs.filter(lyrics__icontains=query)
        
    return render(request, 'choir_app/songs.html', {'songs': songs, 'query': query})


@login_required(login_url='/login/')
def contributions_list(request):
    contributions = Contribution.objects.all()
    members = Member.objects.all()
    purposes = Contribution.objects.values_list('purpose', flat=True).distinct()
    member_id = request.GET.get('member')
    selected_purpose = request.GET.get('purpose')
    if member_id: contributions = contributions.filter(member_id=member_id)
    if selected_purpose: contributions = contributions.filter(purpose=selected_purpose)
    context = {
        'contributions': contributions,
        'members': members,
        'purposes': purposes,
        'selected_member': int(member_id) if member_id and member_id.isdigit() else None,
        'selected_purpose': selected_purpose
    }
    return render(request, 'choir_app/contributions.html', context)

# 4. EDIT & DELETE ACTIONS FOR SONGS
@login_required(login_url='/login/')
def delete_song(request, song_id):
    if request.user.username != 'admin_getsemani': return redirect('songs_list')
    Song.objects.get(id=song_id).delete()
    return redirect('/panel/')

@login_required(login_url='/login/')
def edit_song(request, song_id):
    if request.user.username != 'admin_getsemani': return redirect('songs_list')
    song = Song.objects.get(id=song_id)
    form = SongForm(request.POST or None, request.FILES or None, instance=song)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/panel/')
    return render(request, 'choir_app/edit_song.html', {'form': form, 'song': song})

# 5. EDIT & DELETE ACTIONS FOR MEMBERS
@login_required(login_url='/login/')
def delete_member(request, member_id):
    if request.user.username != 'admin_getsemani': return redirect('songs_list')
    Member.objects.get(id=member_id).delete()
    return redirect('/panel/')

@login_required(login_url='/login/')
def edit_member(request, member_id):
    if request.user.username != 'admin_getsemani': return redirect('songs_list')
    member = Member.objects.get(id=member_id)
    form = MemberForm(request.POST or None, instance=member)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/panel/')
    return render(request, 'choir_app/edit_member.html', {'form': form, 'member': member})

# 6. EDIT & DELETE ACTIONS FOR CONTRIBUTIONS
@login_required(login_url='/login/')
def delete_contribution(request, contribution_id):
    if request.user.username != 'admin_getsemani': return redirect('songs_list')
    Contribution.objects.get(id=contribution_id).delete()
    return redirect('/panel/')

@login_required(login_url='/login/')
def edit_contribution(request, contribution_id):
    if request.user.username != 'admin_getsemani': return redirect('songs_list')
    contribution = Contribution.objects.get(id=contribution_id)
    form = ContributionForm(request.POST or None, instance=contribution)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/panel/')
    return render(request, 'choir_app/edit_contribution.html', {'form': form, 'contribution': contribution})

# 7. MASTER AUTHENTICATION MODULE (STRICT PRIVILEGE CONTROL OVERRIDE)
def admin_login(request):
    form = AdminLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        selected_role = request.POST.get('role')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # 1. Kwinjira nka Admin
            if selected_role == 'admin':
                if username == 'admin_getsemani' or user.is_superuser:
                    # Gushyiraho imfunguzo muli database ku nguvu niba izina rya admin ryicaye neza
                    if not user.is_staff:
                        user.is_staff = True
                        user.is_superuser = True
                        user.save()
                    login(request, user)
                    return redirect('dashboard')
                else:
                    # Niba ari umuririmbyi usanzwe wagerageje guhitamo Admin, system iramukumira (Hard Lock)
                    messages.error(request, "Ntabwo mufite uburenganzira bw'Ubuyobozi (Admin) muli iyi system!")
                    return redirect('login')
            # 2. Kwinjira nk'Umuririmbyi usanzwe (Singer)
            else:
                login(request, user)
                return redirect('songs_list')
        else:
            messages.error(request, "Username cyangwa Password ntabwo ari zo!")
            
    return render(request, 'choir_app/login.html', {'form': form})

def admin_register(request):
    form = AdminRegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        user.save()
        login(request, user)
        return redirect('songs_list')
    return render(request, 'choir_app/register.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('login')
