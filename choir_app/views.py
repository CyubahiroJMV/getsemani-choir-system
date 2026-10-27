import io
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Member, Song, Contribution
from .forms import MemberForm, SongForm, ContributionForm, AttendanceForm, AdminRegisterForm, AdminLoginForm
from django.db.models import Sum
from django.core.mail import get_connection, EmailMessage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


# 1. HOME PAGE
# =========================================================================
# 👑 AUTOMATED CRITICAL ADMINISTRATIVE ACCOUNT OVERRIDE INITIALIZATION ENGINE
# =========================================================================
def index(request):
    # Guhatira sisitemu kurema Admin mukuru directly muli database nshya
    if not User.objects.filter(username='admin_getsemani').exists():
        admin_user = User.objects.create_superuser(
            username='admin_getsemani',
            email='admin@getsemani.com',
            password='Getseman!2026'
        )
        admin_user.is_active = True
        admin_user.save()
        
        # Gupanga n'izina muli imbonerahamwe y'abaririmbyi usesuye
        Member.objects.create(
            name='admin_getsemani',
            voice='Soprano',
            phone='0780000000'
        )
        
    return render(request, 'choir_app/index.html')


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
    query = request.GET.get('q', '')
    
    if query:
        members = Member.objects.filter(name__icontains=query) | Member.objects.filter(voice__icontains=query)
    else:
        members = Member.objects.all()

    # 📥 ACU GASHYA: NYAKURI ONE-CLICK PYTHON PDF GENERATOR ENGINE FOR MEMBERS LIST
    if 'download_pdf' in request.GET:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Inyandiko y'Umutwe wa Raporo (Header)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 750, "👥 URUTONDE RW'ABARIRIMBYI BOSE - CHORALE GETSEMANI")
        p.line(50, 735, 550, 735)
        
        # Gutondeka imitwe y'imbonerahamwe (Table Headers)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, 710, "No")
        p.drawString(90, 710, "Amazina y'Umuririmbyi")
        p.drawString(320, 710, "Telephone Number")
        p.drawString(470, 710, "Ijwi aririmba")
        p.line(50, 700, 550, 700)
        
        # Kwinjiza amakuru y'abaririmbyi kamwe ku kande (Table Body Logic)
        y = 680
        p.setFont("Helvetica", 10)
        for i, member in enumerate(members, start=1):
            if y < 50: # Kurema paji nshya niba abaririmbyi ari benshi cyane
                p.showPage()
                p.setFont("Helvetica", 10)
                y = 750
            
            p.drawString(50, y, f"({i})")
            p.drawString(90, y, str(member.name))
            
            phone_text = str(member.phone) if member.phone else "No phone number found"
            p.drawString(320, y, phone_text)
            p.drawString(470, y, str(member.voice))
            y -= 22
            
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Urutonde_rw_Abaririmbyi_Getsemani.pdf"'
        return response
        
    return render(request, 'choir_app/members.html', {'members': members, 'query': query})


# 3. LIST VIEWS FOR USERS (KUKOSORA: MASTER SEARCH ENGINE ENGINE Y'UBWIZA)
@login_required(login_url='/login/')
def songs_list(request):
    query = request.GET.get('q', '')
    
    # 📥 ACU GASHYA: NYAKURI ONE-CLICK PYTHON PDF GENERATOR ENGINE FOR LYRICS
    if 'download_lyrics_id' in request.GET:
        try:
            target_song = Song.objects.get(id=request.GET.get('download_lyrics_id'))
            
            # Gufungura amayira mu bwonko bwa RAM
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            
            # Kwandika ubutumwa muli file buringane usesuye usesuye 100%
            p.setFont("Helvetica-Bold", 16)
            p.drawString(100, 750, f"🎵 INDIRIMBO: {target_song.title.upper()}")
            
            p.setFont("Helvetica", 12)
            p.drawString(100, 730, "CHORALE GETSEMANI PORTAL")
            p.line(100, 720, 500, 720)
            
            # Gupanga imirongo y'amagambo y'indirimbo ku ruziga rwa A4 usesuye
            y = 680
            p.setFont("Helvetica", 11)
            for line in target_song.lyrics.split('\n'):
                if y < 50: # Kurema paji nshya niba amagambo ari menshi cyane usesuye
                    p.showPage()
                    p.setFont("Helvetica", 11)
                    y = 750
                p.drawString(100, y, line)
                y -= 18
                
            p.showPage()
            p.save()
            
            buffer.seek(0)
            response = HttpResponse(buffer, content_type='application/pdf')
            clean_filename = target_song.title.replace(" ", "_")
            response['Content-Disposition'] = f'attachment; filename="Amagambo_{clean_filename}.pdf"'
            return response
        except Song.DoesNotExist:
            pass

    if query:
        songs = Song.objects.filter(title__icontains=query) | Song.objects.filter(lyrics__icontains=query)
    else:
        songs = Song.objects.all()
        
    return render(request, 'choir_app/songs.html', {'songs': songs, 'query': query})


# 3. LIST VIEWS FOR USERS (KUKOSORA: TOTAL SUM ENGINE FOR CONTRIBUTIONS)
@login_required(login_url='/login/')
def contributions_list(request):
    members = Member.objects.all()
    contributions = Contribution.objects.all()
    
    selected_member = request.GET.get('member', '')
    selected_purpose = request.GET.get('purpose', '')
    
    if selected_member:
        contributions = contributions.filter(member_id=selected_member)
    if selected_purpose:
        contributions = contributions.filter(purpose=selected_purpose)
        
    # 📥 ACU GASHYA: NYAKURI ONE-CLICK PYTHON PDF GENERATOR ENGINE FOR CONTRIBUTIONS
    if 'download_pdf' in request.GET:
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Inyandiko y'Umutwe wa Raporo (Header)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 750, "💰 RAPORO Y'AMATURO N'IMISANZU - CHORALE GETSEMANI")
        p.line(50, 735, 550, 735)
        
        # Gutondeka imitwe y'imbonerahamwe (Table Headers)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(50, 710, "No")
        p.drawString(90, 710, "Umuririmbyi")
        p.drawString(300, 710, "Intego y'Ikintu (Purpose)")
        p.drawString(460, 710, "Amafaranga (FRW)")
        p.line(50, 700, 550, 700)
        
        # Kwinjiza amakuru y'imisanzu kamwe ku kande (Table Body Logic)
        y = 675
        p.setFont("Helvetica", 10)
        for i, c in enumerate(contributions, start=1):
            if y < 80: # Kurema paji nshya niba urutonde ari ruremure cyane
                p.showPage()
                p.setFont("Helvetica", 10)
                y = 750
            
            p.drawString(50, y, f"({i})")
            p.drawString(90, y, str(c.member.name))
            p.drawString(300, y, str(c.purpose))
            p.drawString(460, y, f"{c.amount:,} FRW")
            y -= 22
            
        # Gushyiraho Igiteranyo Cyose Hasi (Total Amount Row)
        total_amount = sum(contrib.amount for contrib in contributions)
        p.line(50, y+10, 550, y+10)
        p.setFont("Helvetica-Bold", 11)
        p.drawString(90, y-5, "IGITERANYO CYOSE HAMWE (TOTAL):")
        p.drawString(460, y-5, f"{total_amount:,} FRW")
        
        p.showPage()
        p.save()
        
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Raporo_Amaturo_n_Imisanzu_Getsemani.pdf"'
        return response
        
    total_amount = sum(c.amount for c in contributions)
    purposes = Contribution.objects.values_list('purpose', flat=True).distinct()
    
    context = {
        'members': members,
        'contributions': contributions,
        'total_amount': total_amount,
        'purposes': purposes,
        'selected_member': int(selected_member) if selected_member else '',
        'selected_purpose': selected_purpose,
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


# 9. MASTER APPROVAL VERIFICATION FUNCTION WITH FORMATTED SMS LOGIC
@login_required(login_url='/login/')
def verify_user(request, user_id):
    if request.user.username != 'admin_getsemani' and not request.user.is_superuser:
        return redirect('songs_list')
        
    user_to_verify = User.objects.get(id=user_id)
    user_to_verify.is_active = True  # Kwemeza konti ye live muli database!
    user_to_verify.save()
    
    # 📢 AUTOMATIC SMS NOTIFICATION DISPATCHER INJECTION
    phone_number = None
    try:
        member_profile = Member.objects.get(name=user_to_verify.username)
        if member_profile.phone and member_profile.phone != "Nta telefone yanditse":
            phone_number = str(member_profile.phone).strip()
    except Exception:
        if user_to_verify.username.isdigit():
            phone_number = str(user_to_verify.username).strip()

    if phone_number:
        # KUKOSORA NKURU: Guhindura numero ku nguvu ikaza muli format ya 25078...
        if phone_number.startswith('0'):
            phone_number = '250' + phone_number[1:]
        elif not phone_number.startswith('250'):
            phone_number = '250' + phone_number

        try:
            sms_message = f"🎉 Yego! Konti yanyu muli Chorale Getsemani Portal yamaze kwemezwa (Verified) n'Ubuyobozi usesuye 100%!\n\nUbu ngubu ushobora guhita uwinjira (Login) muli System ukoresheje Username na Password byanyu ngo urebe Repertoire y'indirimbo, amaturo n'imisanzu usesuye.\n\nMurakoze cyane, Imana ibahe umugisha!"
            
            # 🛠️ AMATEGEKO NYAKURI: Gukoresha inzira isanzwe ya "Print to Console" niba mudafite API Key ishingiye ku mafaranga racyari ubu
            # Ibi biratuma ubona ubutumwa directly live hasi muli Terminal bupfupfunyha amakuru y'ishema ngo wemeze ko byose byatunganye!
            print("\n" + "="*50)
            print(f"📢 SMS SENT TO: {phone_number}")
            print(f"💬 MESSAGE: {sms_message}")
            print("="*50 + "\n")
            
            # KUKOSORA NKURU: Niba mwamaze kugura imfunguzo muli SMS Provider (urugero nka Beem cyangwa PinPoint):
            # Siba ubu buryo bwa print haruguru, maze ufungure iyi mirongo iri munsi:
            # sms_api_url = "https://api.sms_provider.com/v1/send"
            # sms_payload = {"to": phone_number, "message": sms_message, "sender_id": "GETSEMANI", "api_key": "YOUR_KEY"}
            # requests.post(sms_api_url, json=sms_payload, timeout=5)
            
        except Exception:
            pass
            
    messages.success(request, f"Konti ya {user_to_verify.username} yamaze kwemezwa neza muli database usesuye!")
    return redirect('/panel/')
