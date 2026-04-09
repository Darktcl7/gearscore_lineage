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
    path('board/reset-lifetime/', views.dkp_reset_lifetime, name='dkp-reset-lifetime'),
    path('my-profile/', views.dkp_my_profile, name='web-dkp-my-profile'),
    path('profile/<int:user_id>/', views.dkp_user_profile, name='web-dkp-user-profile'),
    path('manage/', views.dkp_manage, name='web-dkp-manage'),
    path('manage/boss-config/', views.boss_point_config_get, name='boss-config-get'),
    path('manage/boss-config/save/', views.boss_point_config_save, name='boss-config-save'),
    path('manage/event/<int:event_id>/attendance/', views.dkp_attendance_list, name='web-dkp-attendance'),
    path('reset-data/', views.dkp_reset_data, name='reset-dkp-data'),

    # TREASURY SYSTEM
    path('treasury/', views.treasury_page, name='web-dkp-treasury'),
    path('treasury/config/', views.treasury_config_get, name='treasury-config-get'),
    path('treasury/config/save/', views.treasury_config_save, name='treasury-config-save'),
    path('treasury/request/', views.treasury_request_item, name='treasury-request-item'),
    path('treasury/reject/', views.treasury_reject_request, name='treasury-reject-request'),
    path('treasury/assign/', views.treasury_assign, name='treasury-assign'),
    path('treasury/delete-logs/', views.treasury_delete_logs, name='treasury-delete-logs'),

    # AUCTION SYSTEM (APIs for Discord Bot)
    path('api/auction/bid/', views.api_auction_bid, name='api-auction-bid'),
    path('api/auction/active/', views.api_auction_active, name='api-auction-active'),
    path('api/auction/check-expired/', views.api_auction_check_expired, name='api-auction-check-expired'),
]
