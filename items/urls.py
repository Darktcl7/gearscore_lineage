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
    my_activity,
    manage_events,
    create_event,
    record_attendance,
    # Discord Link
    link_discord,
    reset_password_admin, # Admin Reset Password
    update_prize_config, # Activity Views - Update Config
    discord_dashboard, # Discord Management
) 

urlpatterns = [
    # ===============================================
    # 1. ITEM VIEWS (Daftar & Formulir Item)
    # ===============================================
    
    # URL: /items/activity/config/update/ -> Update Prize Config
    path('activity/config/update/', update_prize_config, name='update-prize-config'),
    
    # URL: /items/items/ -> Menampilkan daftar semua item
    path('items/', item_list, name='item-list'), 
    
    # URL: /items/item/new/ -> Formulir untuk membuat item baru
    path('item/new/', create_item, name='create-item'), 

    # URL: /items/manage/ -> Halaman Manajemen Karakter (Admin)
    path('manage/', character_management, name='character-management'),

    # URL: /items/manage/reset-password/1/ -> Reset Password User via Admin
    path('manage/reset-password/<int:user_pk>/', reset_password_admin, name='reset-password-admin'),
    
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
    
    # URL: /items/activity/my/ -> My Activity (User's own stats)
    path('activity/my/', my_activity, name='my-activity'),
    
    # URL: /items/activity/events/ -> Admin: Manage Events
    path('activity/events/', manage_events, name='manage-events'),
    
    # URL: /items/activity/events/new/ -> Admin: Create Event
    path('activity/events/new/', create_event, name='create-event'),
    
    # URL: /items/activity/events/1/attendance/ -> Admin: Record Attendance
    path('activity/events/<int:event_pk>/attendance/', record_attendance, name='record-attendance'),

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
    
    # ===============================================
    # 6. DISCORD LINK
    # ===============================================
    
    # URL: /items/profile/1/discord/ -> Link Discord to Character
    # URL: /items/profile/1/discord/ -> Link Discord to Character
    path('profile/<int:character_pk>/discord/', link_discord, name='link-discord'),

]
