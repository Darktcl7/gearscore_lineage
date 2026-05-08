# Fix untuk Gambar Event Icons dan Background yang Tidak Muncul di Production

## Masalah
Gambar event icons dan background image tidak muncul di website production (valkyrie.id) meskipun sudah muncul di localhost.

## Penyebab
1. **Struktur folder static tidak konsisten**: Ada dua struktur berbeda
   - `items/static/images/` (struktur lama - SALAH)
   - `items/static/items/images/` (struktur yang benar - BENAR)

2. **Path di model dan template tidak sesuai**: Model `get_icon_url` mengembalikan path tanpa prefix `items/`

3. **JavaScript di create_event.html menggunakan path lama**: `/static/images/events/` (SALAH)

## Solusi yang Sudah Diterapkan

### 1. Update Model (items/models.py)
✅ Method `get_icon_url` sudah diupdate untuk mengembalikan path dengan prefix `items/`:
```python
'BOSS_RUSH': 'items/images/events/boss_rush.png',
```

### 2. Reorganisasi Struktur Folder Static
✅ File sudah disalin ke struktur yang benar:
- `items/static/items/images/events/` - semua event icons
- `items/static/items/images/tiers/` - semua tier badges
- `items/static/items/images/bg_main.jpeg` - background image

### 3. Update Template HTML
✅ Semua template sudah diupdate untuk menggunakan path yang benar:
```html
{% static 'items/images/events/raid.png' %}
{% static 'items/images/tiers/tier_core.png' %}
{% static 'items/images/bg_main.jpeg' %}
```

### 4. Update JavaScript di create_event.html
✅ Path icon preview di JavaScript sudah diupdate:
```javascript
iconPreview.src = "/static/items/images/events/" + iconMap[evType];
```

## Langkah Deploy ke Production Server

### 1. Push perubahan ke Git
```bash
git add .
git commit -m "Fix: Update create_event.html icon preview path"
git push origin main
```

### 2. Di Server Production (SSH ke valkyrie.id)
```bash
cd /home/valkyrie.id/public_html && \
git checkout -- discord_bot/bot_log.txt && \
git pull origin main && \
source venv/bin/activate && \
rm -rf staticfiles/* && \
python manage.py collectstatic --noinput --clear && \
{ pkill -f "gunicorn.*myproject.wsgi" || true; } && \
sleep 2 && \
gunicorn --workers 3 --bind 127.0.0.1:8001 --timeout 120 --daemon myproject.wsgi:application && \
echo "DONE - check files:" && \
ls -la staticfiles/items/images/events/ && \
ls -la staticfiles/items/images/tiers/ && \
ls -la staticfiles/items/images/bg_main*
```

### 3. Verifikasi File di Server
```bash
# Cek apakah file event icons ada di lokasi yang benar
ls -la /home/valkyrie.id/public_html/staticfiles/items/images/events/

# Cek apakah file tier badges ada
ls -la /home/valkyrie.id/public_html/staticfiles/items/images/tiers/

# Cek background image
ls -la /home/valkyrie.id/public_html/staticfiles/items/images/bg_main.jpeg
```

### 4. Clear Browser Cache
Setelah deploy, **WAJIB** clear browser cache atau buka website dalam **incognito mode** untuk memastikan gambar baru dimuat.

**Cara Clear Cache:**
- Chrome/Edge: `Ctrl + Shift + Delete` → Clear cached images and files
- Firefox: `Ctrl + Shift + Delete` → Cached Web Content
- Atau gunakan: `Ctrl + Shift + R` untuk hard reload
- Atau buka dalam **Incognito/Private Mode**

## File yang Diubah
1. ✅ `items/models.py` - Method `get_icon_url`
2. ✅ `items/templates/items/my_activity.html` - Path event icons dan tier badges
3. ✅ `items/templates/items/raid_boss_activity.html` - Path event icons
4. ✅ `items/templates/items/admin_all_members_activity.html` - Path tier badges
5. ✅ `items/templates/items/activity_leaderboard.html` - Path tier badges
6. ✅ `items/templates/items/manage_events.html` - Menggunakan `event.get_icon_url`
7. ✅ `items/templates/items/create_event.html` - JavaScript icon preview path
8. ✅ `items/templates/items/base.html` - Background image path (sudah benar)
9. ✅ Struktur folder: `items/static/items/images/events/` dan `items/static/items/images/tiers/`

## Catatan Penting
- ⚠️ Folder lama `items/static/images/` masih ada tapi tidak digunakan lagi
- ⚠️ Setelah deploy, pastikan menjalankan `collectstatic` untuk mengumpulkan file ke `staticfiles/`
- ⚠️ Jika menggunakan CDN atau caching, pastikan untuk clear cache CDN juga
- ⚠️ **WAJIB clear browser cache** setelah deploy untuk melihat perubahan

## Testing
Setelah deploy dan clear browser cache, test URL berikut:
- https://valkyrie.id/portal/activity/events/ - Event icons di tabel
- https://valkyrie.id/portal/activity/events/new/ - Event icon preview saat pilih event type
- https://valkyrie.id/portal/activity/my/ - Tier badges dan event icons
- Background image `bg_main.jpeg` harus muncul di semua halaman

Gambar event icons, tier badges, dan background image seharusnya sudah muncul dengan benar.
