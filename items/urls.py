# D:\Django Project\Alto Project\items\urls.py - Trigger Reload

from django.urls import path, include
# Impor SEMUA fungsi view yang telah kita buat
from .views import (
    item_list, 
    item_detail, 
    create_item, 
    character_list, 
    character_management, # New View
    character_profile, 
    create_character,
    edit_subclass_stats,        # Form Edit Subclass Stats
    delete_character,           # Hapus Karakter
    edit_item,                  # Edit Item
    delete_item,                # Hapus Item
    edit_characteristics_stats, # Edit Characteristics
    # Activity Views
    activity_leaderboard,
    gearscore_leaderboard,
    my_activity,
    manage_events,
    create_event,
    record_attendance,
    scan_party_for_event,
    duplicate_event,
    toggle_event_repeatable,
    # Discord Link
    link_discord,
    reset_password_admin, # Admin Reset Password
    toggle_admin, # Admin Toggle Admin Status
    update_prize_config, # Activity Views - Update Config
    admin_adjust_score, # Activity Views - Admin Score Adjustment
    reset_leaderboard_data,
    reset_monthly_rewards, # Admin Reset Monthly Rewards
    discord_dashboard, # Discord Management
    complete_event, # Complete Event with result
    toggle_sub_admin, # Toggle Sub Admin
    toggle_admin_role, # Toggle granular roles
    # Universal Power Rank
    power_rank_leaderboard,
    edit_power_rank,
    delete_power_rank_screenshot,
    update_power_rank_validation,
    update_power_rank_farm_snapshot,
    
    # Activity - Admin All Members
    admin_all_members_activity,
    
    # Hall of Fame
    hall_of_fame_view,
    manage_hall_of_fame,
    
    # Soul System
    soul_page,
    toggle_soul,
    verify_soul,
    bulk_verify_souls,
    upload_soul_proof,
    delete_soul_proof,
    batch_update_souls,
) 

import dkp.views as dkp_views

urlpatterns = [
    # ===============================================
    # 1. ITEM VIEWS (Daftar & Formulir Item)
    # ===============================================
    
    # URL: /items/activity/config/update/ -> Update Prize Config
    path('activity/config/update/', update_prize_config, name='update-prize-config'),
    
    # URL: /items/activity/adjust-score/ -> Admin Adjust Score
    path('activity/adjust-score/', admin_adjust_score, name='admin-adjust-score'),
    
    # URL: /items/activity/reset-data/ -> Admin Reset Data
    path('activity/reset-data/', reset_leaderboard_data, name='reset-leaderboard-data'),
    
    # URL: /items/items/ -> Menampilkan daftar semua item
    path('items/', item_list, name='item-list'), 
    
    # URL: /items/item/new/ -> Formulir untuk membuat item baru
    path('item/new/', create_item, name='create-item'), 

    # URL: /items/manage/ -> Halaman Manajemen Karakter (Admin)
    path('manage/', character_management, name='character-management'),

    # URL: /items/manage/reset-password/1/ -> Reset Password User via Admin
    path('manage/reset-password/<int:user_pk>/', reset_password_admin, name='reset-password-admin'),

    # URL: /items/manage/toggle-admin/1/ -> Toggle Admin Status
    path('manage/toggle-admin/<int:user_pk>/', toggle_admin, name='toggle-admin'),

    path('manage/toggle-sub-admin/<int:user_pk>/', toggle_sub_admin, name='toggle-sub-admin'),
    path('manage/toggle-admin-role/<int:user_pk>/', toggle_admin_role, name='toggle-admin-role'),
    
    # Manage Auction
    path('manage/auction/', dkp_views.auction_page, name='web-portal-auction'),
    path('manage/auction/create/', dkp_views.auction_create, name='auction-create'),
    path('manage/auction/start/', dkp_views.auction_start, name='auction-start'),
    path('manage/auction/cancel/', dkp_views.auction_cancel, name='auction-cancel'),
    path('manage/auction/delete/', dkp_views.auction_delete, name='auction-delete'),
    path('manage/auction/clear-winners/', dkp_views.auction_clear_winners, name='auction-clear-winners'),
    path('manage/auction/poll-times/', dkp_views.auction_poll_times, name='auction-poll-times'),
    
    # URL: /items/item/1/ -> Menampilkan detail satu item
    path('item/<int:pk>/', item_detail, name='item-detail'),
    
    # URL: /items/item/edit/1/ -> Formulir untuk mengedit item
    path('item/edit/<int:pk>/', edit_item, name='edit-item'),
    
    # URL: /items/item/delete/1/ -> Halaman konfirmasi untuk menghapus item
    path('item/delete/<int:pk>/', delete_item, name='delete-item'),
    
    
    # ===============================================
    # 2. CHARACTER VIEWS (Daftar & Profil Karakter)
    # ===============================================
    
    # URL: /items/profiles/ -> Menampilkan daftar semua karakter
    path('profiles/', character_list, name='character-list'),
    
    # URL: /items/profile/1/ -> Menampilkan detail profil dan Gear Score
    path('profile/<int:pk>/', character_profile, name='character-profile'),
    
    # URL: /items/character/new/ -> Formulir untuk membuat karakter baru
    path('character/new/', create_character, name='create-character'),
    
    # URL: /items/character/edit/1/ -> Formulir untuk mengedit karakter (termasuk perlengkapan)
    path('character/edit/<int:pk>/', create_character, name='edit-character'),
    
    # URL: /items/character/1/delete/ -> Halaman konfirmasi untuk menghapus karakter
    path('character/<int:pk>/delete/', delete_character, name='delete-character'),
    
    
    # ===============================================
    # 3. STATISTIK TAMBAHAN (Sesuai Struktur Website Referensi)
    # ===============================================
    
    # URL: /items/profile/1/subclass/ -> Formulir untuk mengedit Subclass Stats
    path('profile/<int:character_pk>/subclass/', edit_subclass_stats, name='edit-subclass-stats'),

    # URL: /items/profile/1/characteristics/ -> Formulir untuk mengedit Characteristics Stats
    path('profile/<int:character_pk>/characteristics/', edit_characteristics_stats, name='edit-characteristics-stats'),
    
    # ===============================================
    # 4. ACTIVITY VIEWS (Tracking Aktivitas Guild)
    # ===============================================
    
    # URL: /items/activity/ -> Leaderboard Activity
    path('activity/', activity_leaderboard, name='activity-leaderboard'),
    
    # URL: /items/gearscore/ -> Leaderboard Gear Score
    path('gearscore/', gearscore_leaderboard, name='gearscore-leaderboard'),
    
    # URL: /items/activity/my/ -> My Activity (User's own stats)
    path('activity/my/', my_activity, name='my-activity'),
    
    # URL: /items/activity/my/1/ -> Super Admin: View specific member's activity
    path('activity/my/<int:character_pk>/', my_activity, name='member-activity'),
    
    # URL: /items/activity/all-members/ -> Super Admin: View all members list
    path('activity/all-members/', admin_all_members_activity, name='admin-all-members-activity'),
    
    # URL: /items/activity/rewards/reset/ -> Admin: Reset Monthly Rewards
    path('activity/rewards/reset/', reset_monthly_rewards, name='reset-monthly-rewards'),
    
    # URL: /items/activity/events/ -> Admin: Manage Events
    path('activity/events/', manage_events, name='manage-events'),
    
    # URL: /items/activity/raid-boss/ -> Admin: Raid Boss Activity
    path('activity/raid-boss/', __import__('items.views', fromlist=['raid_boss_activity']).raid_boss_activity, name='raid-boss-activity'),
    
    # URL: /items/activity/ap_adjust/ -> Admin: Adjust AP manually
    path('activity/ap_adjust/', __import__('items.views', fromlist=['adjust_ap']).adjust_ap, name='adjust_ap'),
    
    # URL: /items/activity/score_adjust/ -> Admin: Adjust Score manually
    path('activity/score_adjust/', __import__('items.views', fromlist=['adjust_score']).adjust_score, name='adjust_score'),
    
    # URL: /items/activity/events/new/ -> Admin: Create Event
    path('activity/events/new/', create_event, name='create-event'),

    
    # War Point System
    path('war-point/', __import__('items.views', fromlist=['war_point_page']).war_point_page, name='war-point'),
    path('war-point/manage/', __import__('items.views', fromlist=['war_point_manage']).war_point_manage, name='war-point-manage'),
    path('war-point/analyze-image/', __import__('items.views', fromlist=['analyze_war_image']).analyze_war_image, name='analyze-war-image'),
    
    # Party Scanner System
    path('party-scanner/', __import__('items.views', fromlist=['party_scanner_page']).party_scanner_page, name='party-scanner'),
    path('party-scanner/analyze/', __import__('items.views', fromlist=['analyze_party_image']).analyze_party_image, name='analyze-party-image'),
    
    # URL: /items/activity/events/1/attendance/ -> Admin: Record Attendance
    path('activity/events/<int:event_pk>/attendance/', record_attendance, name='record-attendance'),
    path('activity/events/<int:event_pk>/party-scan/', scan_party_for_event, name='scan-party-for-event'),

    # URL: /items/activity/events/1/duplicate/ -> Admin: Duplicate Event
    path('activity/events/<int:event_pk>/duplicate/', duplicate_event, name='duplicate-event'),

    # URL: /items/activity/events/1/toggle-repeat/ -> Admin: Toggle Repeatable
    path('activity/events/<int:event_pk>/toggle-repeat/', toggle_event_repeatable, name='toggle-event-repeatable'),

    # URL: /items/activity/events/1/complete/ -> Admin: Complete Event with result
    path('activity/events/<int:event_pk>/complete/', complete_event, name='complete-event'),

    # URL: /items/manage/discord/ -> Discord Control Center
    path('manage/discord/', discord_dashboard, name='discord-dashboard'),
    
    
    # ===============================================
    # 5. API ENDPOINTS (Discord Bot Integration)
    # ===============================================
    
    # API: Create Event
    path('api/activity/event/create/', 
         __import__('items.api_views', fromlist=['api_create_event']).api_create_event, 
         name='api-create-event'),
    
    # API: Record Check-in
    path('api/activity/checkin/', 
         __import__('items.api_views', fromlist=['api_record_checkin']).api_record_checkin, 
         name='api-checkin'),
    
    # API: Complete Event
    path('api/activity/event/complete/', 
         __import__('items.api_views', fromlist=['api_complete_event']).api_complete_event, 
         name='api-complete-event'),
    
    # API: Get Leaderboard
    path('api/activity/leaderboard/', 
         __import__('items.api_views', fromlist=['api_get_leaderboard']).api_get_leaderboard, 
         name='api-leaderboard'),
    
    # API: Get Player Stats
    path('api/activity/player/<str:character_name>/', 
         __import__('items.api_views', fromlist=['api_player_stats']).api_player_stats, 
         name='api-player-stats'),

    # API: Get Player Stats (Discord ID)
    path('api/activity/player/discord/<str:discord_id>/', 
         __import__('items.api_views', fromlist=['api_player_stats_discord']).api_player_stats_discord, 
         name='api-player-stats-discord'),
    
    # API: Get Active Events
    path('api/activity/events/active/', 
         __import__('items.api_views', fromlist=['api_get_active_events']).api_get_active_events, 
         name='api-active-events'),
         
    # API: Delete Event
    path('api/activity/event/delete/', 
         __import__('items.api_views', fromlist=['api_delete_event']).api_delete_event, 
         name='api-delete-event'),

    # API: Toggle Event Status (Completed/Open)
    path('api/activity/event/<int:event_pk>/toggle-status/', 
         __import__('items.api_views', fromlist=['api_toggle_event_status']).api_toggle_event_status, 
         name='api-toggle-event-status'),

    # API: Toggle Event Result (Win/Lose)
    path('api/activity/event/<int:event_pk>/toggle-result/', 
         __import__('items.api_views', fromlist=['api_toggle_event_result']).api_toggle_event_result, 
         name='api-toggle-event-result'),

    # API: Update Event Result (Detailed, e.g., Invasion Bosses)
    path('api/activity/event/<int:event_pk>/update-result/', 
         __import__('items.api_views', fromlist=['api_update_event_result']).api_update_event_result, 
         name='api-update-event-result'),

    # API: Discord Alarms
    path('api/discord/alarms/', 
         __import__('items.api_views', fromlist=['api_get_discord_alarms']).api_get_discord_alarms, 
         name='api-discord-alarms'),

    # API: Discord Announcements
    path('api/discord/announcements/', 
         __import__('items.api_views', fromlist=['api_check_discord_announcements']).api_check_discord_announcements, 
         name='api-discord-announcements'),
         
    # API: Submit War Point
    path('api/war-point/submit/', 
         __import__('items.api_views', fromlist=['api_submit_war_point']).api_submit_war_point, 
         name='api-submit-war-point'),
    
    # ===============================================
    # 6. DISCORD LINK
    # ===============================================
    
    # URL: /items/profile/1/discord/ -> Link Discord to Character
    # URL: /items/profile/1/discord/ -> Link Discord to Character
    path('profile/<int:character_pk>/discord/', link_discord, name='link-discord'),

    # ===============================================
    # 7. UNIVERSAL POWER RANK
    # ===============================================
    
    # URL: /portal/power-rank/ -> Power Rank Leaderboard
    path('power-rank/', power_rank_leaderboard, name='power-rank-leaderboard'),
    
    # URL: /portal/power-rank/edit/1/ -> Edit Power Rank Stats
    path('power-rank/edit/<int:character_pk>/', edit_power_rank, name='edit-power-rank'),
    
    # URL: /portal/power-rank/screenshot/delete/ -> AJAX: Delete Power Rank Screenshot
    path('power-rank/screenshot/delete/', delete_power_rank_screenshot, name='delete-power-rank-screenshot'),

    # URL: /portal/power-rank/validation/update/ -> AJAX: Update Validation Admin
    path('power-rank/validation/update/', update_power_rank_validation, name='update-power-rank-validation'),

    # URL: /portal/power-rank/farm-snapshot/update/ -> Manual update farm spot snapshot
    path('power-rank/farm-snapshot/update/', update_power_rank_farm_snapshot, name='update-power-rank-farm-snapshot'),

    # ===============================================
    # 8. HALL OF FAME
    # ===============================================
    
    # URL: /portal/hall-of-fame/ -> Hall of Fame Page
    path('hall-of-fame/', hall_of_fame_view, name='hall-of-fame-list'),
    
    # URL: /items/manage/hall-of-fame/ -> Admin Manage Hall of Fame
    path('manage/hall-of-fame/', manage_hall_of_fame, name='manage-hall-of-fame'),

    # ===============================================
    # 9. SOUL SYSTEM
    # ===============================================
    
    # URL: /portal/soul/ -> Soul Page
    path('soul/', soul_page, name='soul-page'),
    
    # AJAX: Toggle soul
    path('soul/toggle/', toggle_soul, name='toggle-soul'),
    
    # AJAX: Verify soul (admin)
    path('soul/verify/', verify_soul, name='verify-soul'),
    
    # AJAX: Bulk verify (admin)
    path('soul/bulk-verify/', bulk_verify_souls, name='bulk-verify-souls'),
    
    # AJAX: Upload soul proof screenshot
    path('soul/upload-proof/', upload_soul_proof, name='upload-soul-proof'),
    
    # AJAX: Delete soul proof screenshot
    path('soul/delete-proof/', delete_soul_proof, name='delete-soul-proof'),

    # AJAX: Batch update souls (new modal flow)
    path('soul/batch-update/', batch_update_souls, name='batch-update-souls'),

]

