# Fix untuk Gambar Event Icons dan Background yang Tidak Muncul di Production

## Masalah
Gambar event icons dan background image tidak muncul di website production (valkyrie.id) meskipun sudah muncul di localhost.

## Penyebab
1. **Struktur folder static tidak konsisten**: Ada dua struktur berbeda
   - `items/static/images/` (struktur lama - SALAH)
   - `items/static/items/images/` (struktur yang benar - BENAR)

2. **Path di model dan template tidak sesuai**: Model `get_icon_url` mengembalikan path tanpa prefix `items/`

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

### 3. Update Template HTML
✅ Semua template sudah diupdate untuk menggunakan path yang benar:
```html
{% static 'items/images/events/raid.png' %}
{% static 'items/images/tiers/tier_core.png' %}
```

## Langkah Deploy ke Production Server

### 1. Push perubahan ke Git
```bash
git add .
git commit -m "Fix: Update static files path untuk event icons dan tier badges"
git push origin main
```

### 2. Di Server Production (SSH ke valkyrie.id)
```bash
# Masuk ke directory project
cd /home/valkyrie.id/public_html

# Pull perubahan terbaru
git pull origin main

# Aktifkan virtual environment
source venv/bin/activate

# Jalankan collectstatic untuk mengumpulkan file static yang baru
python manage.py collectstatic --noinput --clear

# Restart Django/Gunicorn service
sudo systemctl restart gunicorn
# ATAU jika menggunakan supervisor:
# sudo supervisorctl restart django-server
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
Setelah deploy, clear browser cache atau buka website dalam incognito mode untuk memastikan gambar baru dimuat.

## File yang Diubah
1. ✅ `items/models.py` - Method `get_icon_url`
2. ✅ `items/templates/items/my_activity.html` - Path event icons dan tier badges
3. ✅ `items/templates/items/raid_boss_activity.html` - Path event icons
4. ✅ `items/templates/items/admin_all_members_activity.html` - Path tier badges
5. ✅ `items/templates/items/activity_leaderboard.html` - Path tier badges
6. ✅ `items/templates/items/manage_events.html` - Menggunakan `event.get_icon_url`
7. ✅ Struktur folder: `items/static/items/images/events/` dan `items/static/items/images/tiers/`

## Catatan Penting
- ⚠️ Folder lama `items/static/images/` masih ada tapi tidak digunakan lagi
- ⚠️ Setelah deploy, pastikan menjalankan `collectstatic` untuk mengumpulkan file ke `staticfiles/`
- ⚠️ Jika menggunakan CDN atau caching, pastikan untuk clear cache CDN juga

## Testing
Setelah deploy, test URL berikut:
- https://valkyrie.id/portal/activity/events/
- https://valkyrie.id/portal/activity/events/new/
- https://valkyrie.id/portal/activity/my/

Gambar event icons dan tier badges seharusnya sudah muncul dengan benar.
