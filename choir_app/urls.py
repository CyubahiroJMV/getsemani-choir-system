from django.urls import path
from . import views

urlpatterns = [
    # 1. HOME PAGE
    path('', views.index, name='index'),
    
    # 2. MASTER DASHBOARD PANEL Y'ABAYOBOZI (TWAHOYOYE INZIRA NGO NOT FOUND ZISHIRE)
    path('panel/', views.dashboard, name='dashboard'),
    
    # 3. LIST VIEWS FOR USERS
    path('members/', views.members_list, name='members_list'),
    path('songs/', views.songs_list, name='songs_list'),
    path('contributions/', views.contributions_list, name='contributions_list'),
    
    # 4. EDIT & DELETE ACTIONS FOR SONGS
    path('delete-song/<int:song_id>/', views.delete_song, name='delete_song'),
    path('edit-song/<int:song_id>/', views.edit_song, name='edit_song'),
    
    # 5. EDIT & DELETE ACTIONS FOR MEMBERS
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('edit-member/<int:member_id>/', views.edit_member, name='edit_member'),
    
    # 6. EDIT & DELETE ACTIONS FOR CONTRIBUTIONS
    path('delete-contribution/<int:contribution_id>/', views.delete_contribution, name='delete_contribution'),
    path('edit-contribution/<int:contribution_id>/', views.edit_contribution, name='edit_contribution'),
    
    # 7. AUTHENTICATIONS
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('register/', views.admin_register, name='register'),
]
