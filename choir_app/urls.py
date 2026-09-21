from django.urls import path
from django.contrib.auth.decorators import login_required # Kwimportinga uburinzi bukomeye bw'inzira
from . import views

urlpatterns = [
    # 1. HOME PAGE (Aha ho uwari we wese yemerewe gukorera no kureba usesuye nta nzitizi)
    path('', views.index, name='index'),
    
    # 2. HARD SECURITY FORCED ROUTES: Inzira zose zafunzwe ku mbaraga zose muli URL LEVEL!
    path('members/', login_required(views.members_list, login_url='login'), name='members_list'),
    path('songs/', login_required(views.songs_list, login_url='login'), name='songs_list'),
    path('contributions/', login_required(views.contributions_list, login_url='login'), name='contributions_list'),
    
    # 3. PANEL N'ABAYOBOZI (ADMIN DASHBOARD)
    path('panel/', login_required(views.dashboard, login_url='login'), name='dashboard'),
    path('admin-panel/', login_required(views.dashboard, login_url='login'), name='admin_dashboard'),
    
    # 4. AUTHENTICATIONS (LOGIN / LOGOUT / REGISTER)
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('register/', views.admin_register, name='register'),
]
