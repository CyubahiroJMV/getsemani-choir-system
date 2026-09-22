from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # 1. HOME PAGE (Aha ho umu-visiteur wese yemerewe kureba usesuye Intego na Vision)
    path('', views.index, name='index'),
    
    # 2. IZHINDI PAJI ZOSE (ZAFUNZWE KU NGUVU KURI URL LEVEL NEZA)
    path('members/', login_required(views.members_list, login_url='/login/'), name='members_list'),
    path('songs/', login_required(views.songs_list, login_url='/login/'), name='songs_list'),
    path('contributions/', login_required(views.contributions_list, login_url='/login/'), name='contributions_list'),
    
    # 3. PANEL N'ABAYOBOZI (ADMIN DASHBOARD)
    path('panel/', login_required(views.dashboard, login_url='/login/'), name='dashboard'),
    path('admin-panel/', login_required(views.dashboard, login_url='/login/'), name='admin_dashboard'),
    
    # 4. AUTHENTICATIONS (LOGIN / LOGOUT / REGISTER)
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('register/', views.admin_register, name='register'),
]
