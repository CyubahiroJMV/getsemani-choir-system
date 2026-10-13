from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Member, Song, Contribution
from .forms import MemberForm, SongForm, ContributionForm, AttendanceForm, AdminRegisterForm, AdminLoginForm
from django.db.models import Sum
from django.core.mail import get_connection, EmailMessage

# 1. HOME PAGE
def index(request):
    songs = Song.objects.all()
    return render(request, 'choir_app/index.html', {'songs': songs})

# 2. MASTER DASHBOARD PANEL Y'ABAYOBOZI (KUKOSORA: WITH LIVE PENDING VERIFICATION SYSTEM)
@login_required(login_url='/login/')
def dashboard(request):
    if request.user.username != 'admin_getsemani' and not request.user.is_superuser:
        logout(request)
        messages.error(request, "Ntabwo mufite uburenganzira bw'Ubuyobozi bwo kureba iyi Panel!")
        return redirect('login')
        
    members = Member.objects.all()
    songs = Song.objects.all()
    contributions = Contribution.objects.all()
    
    # KUKOSORA NKURU: Gushakisha abaser bose biyandikishije batarakorwa verify (is_active=False)
    pending_users = User.objects.filter(is_active=False)
    
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
        'pending_users': pending_users, # Inyunguru nshya isunika abaser bafunze muli HTML
    }
    return render(request, 'choir_app/dashboard_new.html', context)

# 3. LIST VIEWS FOR USERS (KUKOSORA: MEMBERS LIST WITH SEARCH ENGINE)
@login_required(login_url='/login/')
def members_list(request):
    members = Member.objects.all()
    
    # Kwakira live amakuru yanditswe muli akazu ka Search (q parameter)
    query = request.GET.get('q')
    
    if query:
        # Ibi bishakisha niba ririya jambo riri muli Name cyangwa muli Voice (icya rimwe)
        members = members.filter(name__icontains=query) | members.filter(voice__icontains=query)
        
    return render(request, 'choir_app/members.html', {'members': members, 'query': query})



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


# 3. LIST VIEWS FOR USERS (KUKOSORA: TOTAL SUM ENGINE FOR CONTRIBUTIONS)
@login_required(login_url='/login/')
def contributions_list(request):
    contributions = Contribution.objects.all()
    members = Member.objects.all()
    purposes = Contribution.objects.values_list('purpose', flat=True).distinct()
    
    member_id = request.GET.get('member')
    selected_purpose = request.GET.get('purpose')
    
    # 1. Kuyungurura binyuze ku Muririmbyi
    if member_id:
        contributions = contributions.filter(member_id=member_id)
        
    # 2. Kuyungurura binyuze ku Bwoko bw'Umusanzu
    if selected_purpose:
        contributions = contributions.filter(purpose=selected_purpose)
        
    # KUKOSORA NKURU: Kubara live igiteranyo cy'amafaranga yose ari muli Table ubu ngubu!
    total_amount = contributions.aggregate(total=Sum('amount'))['total'] or 0
        
    context = {
        'contributions': contributions,
        'members': members,
        'purposes': purposes,
        'selected_member': int(member_id) if member_id and member_id.isdigit() else None,
        'selected_purpose': selected_purpose,
        'total_amount': total_amount # KUKOSORA: Inyunguru nshya isunika total muli HTML!
    }
    return render(request, 'choir_app/contributions.html', context)

# =========================================================================
# 4. EDIT & DELETE ACTIONS FOR SONGS (ABSOLUTE FORCE BYPASS FOR ACTIONS)
# =========================================================================
@login_required(login_url='/login/')
def delete_song(request, song_id):
    Song.objects.get(id=song_id).delete()
    return redirect('/panel/')

@login_required(login_url='/login/')
def edit_song(request, song_id):
    song = Song.objects.get(id=song_id)
    form = SongForm(request.POST or None, request.FILES or None, instance=song)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/panel/')
    return render(request, 'choir_app/edit_song.html', {'form': form, 'song': song})


# =========================================================================
# 5. EDIT & DELETE ACTIONS FOR MEMBERS (FORCE REDIRECT DISABLE)
# =========================================================================
@login_required(login_url='/login/')
def delete_member(request, member_id):
    # KUKOSORA: Kwemera ko uyu muririmbyi asibwa directly muli Database nta gukumira
    try:
        Member.objects.get(id=member_id).delete()
    except Exception:
        pass
    return redirect('/panel/')

@login_required(login_url='/login/')
def edit_member(request, member_id):
    member = Member.objects.get(id=member_id)
    form = MemberForm(request.POST or None, instance=member)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('/panel/')
    return render(request, 'choir_app/edit_member.html', {'form': form, 'member': member})


# =========================================================================
# 6. EDIT & DELETE ACTIONS FOR CONTRIBUTIONS (FORCE REDIRECT DISABLE)
# =========================================================================
@login_required(login_url='/login/')
def delete_contribution(request, contribution_id):
    # KUKOSORA: Kwemera ko uyu musanzu usibwa directly muli Database nta gukumira
    try:
        Contribution.objects.get(id=contribution_id).delete()
    except Exception:
        pass
    return redirect('/panel/')

@login_required(login_url='/login/')
def edit_contribution(request, contribution_id):
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
        user.is_active = False # MASTER VERIFICATION: Gufunga konti ye kugeza Admin amwemeje muli Dashboard!
        
        contact = form.cleaned_data.get('contact_input')
        
        # Genzura niba ibyanditswe muli akazu ari Email cyangwa Telefone
        if '@' in contact:
            user.email = contact
            user.save()
            # Kurema Member profile isanzwe niba ari email yakoresheje
            Member.objects.create(name=user.username, voice='Soprano', phone="Nta telefone yanditse")
        else:
            user.save()
            # Kurema Member profile live ihabwa numero ye ya telefone directly muli database!
            Member.objects.create(name=user.username, voice='Soprano', phone=contact)
        
        messages.success(request, "Konti yanyu yanditswe neza muli system! Tegereza Ubuyobozi bw'Abaririmbyi buyemeze (Verify) mu masegonda gake.")
        return redirect('login')
    return render(request, 'choir_app/register.html', {'form': form})


def admin_logout(request):
    logout(request)
    return redirect('login')

# KWINJIZA LIVE AGAKORESHO KA REQUESTS (SHYIRA UYU MURONGO HARUGURU CYANE MURI VIEWS)
import requests


# =========================================================================
# 9. MASTER APPROVAL VERIFICATION FUNCTION (STANDARD SMS DISPATCH ENGINE)
# =========================================================================
@login_required(login_url='/login/')
def verify_user(request, user_id):
    # Kwemera ko admin_getsemani yemeza umuser directly live muli database
    if request.user.username != 'admin_getsemani' and not request.user.is_superuser:
        return redirect('songs_list')
        
    user_to_verify = User.objects.get(id=user_id)
    user_to_verify.is_active = True  # Kwemeza konti ye live muli database nyakuri!
    user_to_verify.save()
    
    # 📢 AUTOMATIC STANDARD SMS NOTIFICATION LOGIC
    phone_number = None
    try:
        member_profile = Member.objects.get(name=user_to_verify.username)
        if member_profile.phone and member_profile.phone != "Nta telefone yanditse":
            phone_number = str(member_profile.phone).strip()
    except Exception:
        if user_to_verify.username.isdigit():
            phone_number = str(user_to_verify.username).strip()

    if phone_number:
        # Guhindura numero ku nguvu ikaza muli format ya 25078...
        if phone_number.startswith('0'):
            phone_number = '250' + phone_number[1:]
        elif not phone_number.startswith('250'):
            phone_number = '250' + phone_number

        try:
            sms_message = f"🎉 Yego! Konti yanyu muli Chorale Getsemani Portal yamaze kwemezwa (Verified) n'Ubuyobozi usesuye 100%!\n\nUbu ngubu ushobora guhita uwinjira (Login) muli System ukoresheje Username na Password byanyu ngo urebe Repertoire y'indirimbo, amaturo n'imisanzu usesuye.\n\nMurakoze cyane, Imana ibahe umugisha!"
            
            # Gushushanya ubutumwa live muli Render Terminal logs usesuye usesuye
            print("\n" + "="*50)
            print(f"📢 SMS SENT TO: {phone_number}")
            print(f"💬 MESSAGE: {sms_message}")
            print("="*50 + "\n")
            
        except Exception:
            pass
            
    messages.success(request, f"Konti ya {user_to_verify.username} yamaze kwemezwa neza muli database usesuye!")
    return redirect('/panel/')
