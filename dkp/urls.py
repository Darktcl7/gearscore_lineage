from django.urls import path
from . import views

urlpatterns = [
    # API Endpoints (Prefix: /dkp/api/...)
    path('api/active/', views.api_dkp_active_events, name='dkp_active'),
    path('api/checkin/', views.api_dkp_checkin, name='dkp_checkin'),
    path('api/me/<str:character_name>/', views.api_dkp_me, name='dkp_me'),
    path('api/me/discord/<str:discord_id>/', views.api_dkp_me_discord, name='dkp_me_discord'),
    path('api/leaderboard/', views.api_dkp_leaderboard, name='dkp_leaderboard'),
    
    # Web Views (Accessed via /dkp/...)
    path('board/', views.dkp_leaderboard_web, name='web-dkp-leaderboard'),
    path('board/decay/', views.dkp_decay, name='dkp-decay'),
    path('board/adjust/', views.dkp_adjust, name='dkp-adjust'),
    path('board/give-all/', views.dkp_give_all, name='dkp-give-all'),
    path('board/remove-all/', views.dkp_remove_all, name='dkp-remove-all'),
    path('board/decay-all/', views.dkp_decay_all, name='dkp-decay-all'),
    path('board/give-selected/', views.dkp_give_selected, name='dkp-give-selected'),
    path('board/remove-selected/', views.dkp_remove_selected, name='dkp-remove-selected'),
    path('board/decay-selected/', views.dkp_decay_selected, name='dkp-decay-selected'),
    path('my-profile/', views.dkp_my_profile, name='web-dkp-my-profile'),
    path('profile/<int:user_id>/', views.dkp_user_profile, name='web-dkp-user-profile'),
    path('manage/', views.dkp_manage, name='web-dkp-manage'),
    path('manage/event/<int:event_id>/attendance/', views.dkp_attendance_list, name='web-dkp-attendance'),
]
